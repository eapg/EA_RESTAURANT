from datetime import datetime
from unittest import mock

from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.api.controllers.order_detail_controller import OrderDetailController
from src.api.controllers.product_ingredient_controller import (
    ProductIngredientController,
)

from src.constants.order_status import OrderStatus

from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)

from src.tests.utils.fixtures.kitchen_simulator_fixture import (
    build_kitchen_simulator_running_once,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_chef,
    build_ingredient,
    build_inventory_ingredient,
    build_order,
    build_order_detail,
    build_order_status_history,
    build_product,
    build_product_ingredient,
)
from src.tests.utils.test_util import (
    get_product_ingredient_repository_with_session_pathed,
    get_order_detail_repository_with_session_patched,
    get_inventory_ingredient_repository_with_session_patched,
)


class KitchenSimulatorIntegrationTest(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.iterations = 0

        self.order_detail_controller = OrderDetailController(
            get_order_detail_repository_with_session_patched(self)
        )
        self.product_ingredient_controller = ProductIngredientController(
            get_product_ingredient_repository_with_session_pathed(self)
        )

        self.inventory_ingredient_controller = InventoryIngredientController(
            get_inventory_ingredient_repository_with_session_patched(self)
        )

        self.kitchen_simulator = build_kitchen_simulator_running_once(
            build_app_processor_config()
        )
        self.kitchen_simulator.order_manager = mock.Mock(
            wraps=self.kitchen_simulator.order_manager
        )
        self.kitchen_simulator.chef_controller = mock.Mock(
            wraps=self.kitchen_simulator.chef_controller
        )
        self.kitchen_simulator.order_controller = mock.Mock(
            wraps=self.kitchen_simulator.order_controller
        )
        self.kitchen_simulator.mongo_order_status_history_controller = mock.Mock(
            wraps=self.kitchen_simulator.mongo_order_status_history_controller
        )

    def test_assign_orders_to_available_chefs(self):

        self.kitchen_simulator.process_orders_in_process = mock.Mock()
        self.kitchen_simulator.check_for_order_completed = mock.Mock()
        ingredient_1 = build_ingredient(ingredient_id=1, name="potatoes")

        inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1, ingredient_id=ingredient_1.id
        )
        product_1 = build_product(product_id=1, name="fries potatoes")

        product_ingredient_1 = build_product_ingredient(
            product_ingredient_id=1,
            ingredient_id=ingredient_1.id,
            product_id=product_1.id,
        )

        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        mongo_controller = self.kitchen_simulator.mongo_order_status_history_controller

        mongo_controller.set_next_status_history_by_order_id(order_1.id, order_1.status)
        self.kitchen_simulator.order_controller.add(order_1)
        self.kitchen_simulator.order_manager.add_to_queue(order_1)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_1.id, product_id=product_1.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_1)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER)
        mongo_controller.set_next_status_history_by_order_id(order_2.id, order_2.status)
        self.kitchen_simulator.order_controller.add(order_2)
        self.kitchen_simulator.order_manager.add_to_queue(order_2)
        order_detail_2 = build_order_detail(
            order_detail_id=1, order_id=order_2.id, product_id=product_1.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_2)
        self.product_ingredient_controller.add(product_ingredient_1)
        self.inventory_ingredient_controller.add(inventory_ingredient_1)

        chef_1 = build_chef(chef_id=1, skill=2)
        self.kitchen_simulator.chef_controller.add(chef_1)

        def after_execute(_app_processor_config, _app_context):
            self.kitchen_simulator.destroyed = True

        self.kitchen_simulator.app_processor_config.after_execute = after_execute
        self.kitchen_simulator.chef_controller.get_available_chefs.return_value = [1, 2]
        self.kitchen_simulator.order_controller.get_orders_by_status.return_value = [
            order_1,
            order_2,
        ]
        self.kitchen_simulator.order_controller.get_validated_orders_map.return_value = {
            1: True,
            2: False,
        }

        def queue_side_effect(param):
            if param == OrderStatus.NEW_ORDER.name:
                return order_1.id
            if param == OrderStatus.IN_PROCESS:
                return order_1.id
            return order_2.id

        self.kitchen_simulator.order_manager.get_queue_from_status.side_effect = (
            queue_side_effect
        )

        self.kitchen_simulator.start()
        self.kitchen_simulator.join()

        self.assertEqual(
            self.kitchen_simulator.order_manager.get_queue_from_status(
                OrderStatus.IN_PROCESS
            ),
            order_1.id,
        )
        self.assertEqual(
            self.kitchen_simulator.order_manager.get_queue_from_status(
                OrderStatus.CANCELLED
            ),
            order_2.id,
        )
        order_1.assigned_chef_id = 1
        self.kitchen_simulator.order_controller.get_by_id.return_value = order_1
        order_with_assigned_chef = self.kitchen_simulator.order_controller.get_by_id(
            order_1.id
        )
        self.assertEqual(order_with_assigned_chef.assigned_chef_id, chef_1.id)

    @mock.patch(
        "src.core.engine.processors.kitchen_simulator.compute_order_estimated_time",
        return_value=-1,
    )
    def test_check_for_order_complete(self, _mocked_compute_order_estimated_time):

        ingredient_2 = build_ingredient(ingredient_id=2, name="potatoes")
        inventory_ingredient_2 = build_inventory_ingredient(
            inventory_ingredient_id=2, ingredient_id=ingredient_2.id
        )
        product_2 = build_product(product_id=2, name="fries potatoes")

        product_ingredient_2 = build_product_ingredient(
            product_ingredient_id=2, ingredient_id=ingredient_2.id
        )

        mongo_controller = self.kitchen_simulator.mongo_order_status_history_controller
        order_3 = build_order(order_id=3, status=OrderStatus.NEW_ORDER)
        mongo_controller.set_next_status_history_by_order_id(order_3.id, order_3.status)
        self.kitchen_simulator.order_controller.add(order_3)
        self.kitchen_simulator.order_manager.add_to_queue(order_3)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_3.id, product_id=product_2.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_1)
        order_4 = build_order(order_id=4, status=OrderStatus.NEW_ORDER)
        mongo_controller.set_next_status_history_by_order_id(order_4.id, order_4.status)
        self.kitchen_simulator.order_controller.add(order_4)
        self.kitchen_simulator.order_manager.add_to_queue(order_4)
        order_detail_2 = build_order_detail(
            order_detail_id=1, order_id=order_4.id, product_id=product_2.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_2)
        self.product_ingredient_controller.add(product_ingredient_2)
        self.inventory_ingredient_controller.add(inventory_ingredient_2)

        chef_3 = build_chef(chef_id=3, skill=10)
        self.kitchen_simulator.chef_controller.add(chef_3)

        def after_execute(_app_processor_config, _app_context):
            self.iterations += 1
            if self.iterations == 1:
                self.kitchen_simulator.destroyed = True

        self.kitchen_simulator.app_processor_config.after_execute = after_execute
        order_3.status = OrderStatus.COMPLETED
        self.kitchen_simulator.order_controller.get_by_id.return_value = order_3

        last_order_status_history = build_order_status_history(from_time=datetime.now())
        mongo_controller.get_last_status_history_by_order_id.return_value = (
            last_order_status_history
        )
        self.kitchen_simulator.order_manager.get_queue_from_status.return_value = (
            order_3.id
        )
        self.kitchen_simulator.app_processor_config.after_execute = after_execute
        self.kitchen_simulator.chef_controller.get_available_chefs.return_value = [3, 4]
        self.kitchen_simulator.order_controller.get_orders_by_status.return_value = [
            order_3,
            order_4,
        ]
        self.kitchen_simulator.order_controller.get_validated_orders_map.return_value = {
            3: True,
            4: False,
        }

        self.kitchen_simulator.start()
        self.kitchen_simulator.join()

        self.assertEqual(
            self.kitchen_simulator.order_manager.get_queue_from_status(
                OrderStatus.COMPLETED
            ),
            order_3.id,
        )

        self.kitchen_simulator.order_controller.get_by_id(order_3.id)

        mongo_controller.get_last_status_history_by_order_id.assert_has_calls(
            [mock.call(order_3.id)]
        )
