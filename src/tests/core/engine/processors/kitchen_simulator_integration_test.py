from unittest import TestCase, mock
from src.core.engine.processors.kitchen_simulator import KitchenSimulator
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
)
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.chef_fixture import build_chef
from src.constants.order_status import OrderStatus
from src.constants.cooking_type import CookingType
from src.core.order_manager import ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP
from src.tests.utils.fixtures.product_fixture import build_product
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient
from src.core.ioc import get_ioc_instance

ITERATIONS = 0


class KitchenSimulatorIntegrationTest(TestCase):
    def setUp(self):

        ioc = get_ioc_instance()
        self.order_detail_controller = ioc.get_instance("order_detail_controller")
        self.product_ingredient_controller = ioc.get_instance(
            "product_ingredient_controller"
        )
        self.inventory_ingredient_controller = ioc.get_instance(
            "inventory_ingredient_controller"
        )
        self.app_engine_config = build_app_processor_config()
        self.kitchen_simulator = KitchenSimulator(self.app_engine_config)
        self.kitchen_simulator.order_manager = mock.Mock(
            wraps=self.kitchen_simulator.order_manager
        )
        self.kitchen_simulator.chef_controller = mock.Mock(
            wraps=self.kitchen_simulator.chef_controller
        )
        self.kitchen_simulator.order_controller = mock.Mock(
            wraps=self.kitchen_simulator.order_controller
        )
        self.kitchen_simulator.order_status_history_controller = mock.Mock(
            wraps=self.kitchen_simulator.order_status_history_controller
        )

    def test_assign_orders_to_available_chefs(self):
        ingredient_1 = build_ingredient(ingredient_id=1, name="potatoes")
        inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1,
            ingredient_id=ingredient_1.id,
            ingredient_quantity=10,
        )
        product_1 = build_product(product_id=1, name="fries potatoes")
        product_ingredient_1 = build_product_ingredient(
            id=1,
            ingredient_id=ingredient_1.id,
            product_id=product_1.id,
            quantity=6,
            ingredient_type=CookingType.FRYING,
        )

        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        self.kitchen_simulator.order_status_history_controller.set_next_status_history_by_order_id(
            order_1.id, order_1.status
        )
        self.kitchen_simulator.order_controller.add(order_1)
        self.kitchen_simulator.order_manager.add_to_queue(order_1)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_1.id, product_id=product_1.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_1)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER)
        self.kitchen_simulator.order_status_history_controller.set_next_status_history_by_order_id(
            order_2.id, order_2.status
        )
        self.kitchen_simulator.order_controller.add(order_2)
        self.kitchen_simulator.order_manager.add_to_queue(order_2)
        order_detail_2 = build_order_detail(
            order_detail_id=1, order_id=order_2.id, product_id=product_1.id, quantity=1
        )
        self.order_detail_controller.add(order_detail_2)
        self.product_ingredient_controller.add(product_ingredient_1)
        self.inventory_ingredient_controller.add(inventory_ingredient_1)

        chef_1 = build_chef(chef_id=1, chef_skills=2)
        self.kitchen_simulator.chef_controller.add(chef_1)
        chef_2 = build_chef(chef_id=2, chef_skills=3)
        self.kitchen_simulator.chef_controller.add(chef_2)

        def after_execute(_app_processor_config, _app_context):
            global ITERATIONS
            ITERATIONS += 1
            if ITERATIONS == 2:
                self.kitchen_simulator.destroyed = True

        self.kitchen_simulator.app_processor_config.after_execute = after_execute

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
        order_with_assigned_chef = self.kitchen_simulator.order_controller.get_by_id(
            order_1.id
        )
        self.assertEqual(order_with_assigned_chef.assigned_chef_id, chef_1.id)
        self.assertEqual(order_with_assigned_chef.estimated_time, 15.0)
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_has_calls(
            [mock.call([order_1, order_2]), mock.call([order_2])]
        )
        self.kitchen_simulator.order_controller.get_orders_by_status.assert_has_calls(
            [
                mock.call(
                    OrderStatus.NEW_ORDER,
                    order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                        OrderStatus.NEW_ORDER
                    ],
                ),
                mock.call(
                    OrderStatus.NEW_ORDER,
                    order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                        OrderStatus.NEW_ORDER
                    ],
                ),
            ]
        )
        self.kitchen_simulator.order_controller.reduce_order_ingredients_from_inventory.assert_called_with(
            order_1.id
        )
