from datetime import datetime
from unittest import mock

from src.constants.order_status import OrderStatus
from src.core.engine.processors.kitchen_simulator import KitchenSimulator
from src.core.order_manager import ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP
from src.tests.base_env_config_test import BaseEnvConfigTest
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_chef,
    build_order,
    build_order_status_history,
    build_product_ingredient,
)


class KitchenSimulatorTest(BaseEnvConfigTest):
    def setUp(self):
        super().setUp()
        self.app_engine_config = build_app_processor_config()
        self.kitchen_simulator = KitchenSimulator(self.app_engine_config)
        self.kitchen_simulator.order_manager = mock.Mock()
        self.kitchen_simulator.chef_controller = mock.Mock()
        self.kitchen_simulator.order_controller = mock.Mock()
        self.kitchen_simulator.mongo_order_status_history_repository = mock.Mock()

    @mock.patch(
        "src.core.engine.processors.kitchen_simulator.compute_order_estimated_time"
    )
    def test_assign_orders_to_available_chefs_when_order_is_valid(
        self, mocked_order_estimated_time
    ):

        kitchen_simulator = self.kitchen_simulator
        order_controller = self.kitchen_simulator.order_controller
        chef_1 = build_chef(chef_id=1)
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER.name)

        order_controller.get_orders_by_status.return_value = [order_1]
        order_controller.get_order_ingredients_by_order_id.return_value = [
            build_product_ingredient(
                product_ingredient_id=1,
            )
        ]
        kitchen_simulator.chef_controller.get_available_chefs.return_value = [chef_1]
        order_controller.get_validated_orders_map.return_value = {1: True}
        kitchen_simulator.order_manager.get_queue_size.return_value = 2
        kitchen_simulator.order_manager.get_queue_from_status.return_value = order_1.id
        kitchen_simulator.process_new_orders()
        order_controller.get_orders_by_status.assert_called_with(
            OrderStatus.NEW_ORDER.name,
            order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.NEW_ORDER],
        )
        order_controller.get_validated_orders_map.assert_called_with([order_1])

        kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            OrderStatus.NEW_ORDER.name
        )
        # pylint: disable=W0212
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(
            arg_with_method_was_called[0].status, OrderStatus.IN_PROCESS.name
        )
        mocked_order_estimated_time.asser_called_with(
            [build_product_ingredient(product_ingredient_id=1)],
            chef_1,
        )
        order_controller.reduce_order_ingredients_from_inventory.assert_called_with(
            order_1.id
        )

    def test_assign_orders_to_available_chefs_when_order_is_not_valid(self):
        chef_1 = build_chef(chef_id=1)
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER.name)

        self.kitchen_simulator.order_controller.get_orders_by_status.return_value = [
            order_1
        ]
        self.kitchen_simulator.chef_controller.get_available_chefs.return_value = [
            chef_1
        ]
        self.kitchen_simulator.order_controller.get_validated_orders_map.return_value = {
            1: False
        }
        self.kitchen_simulator.order_manager.get_queue_from_status.return_value = (
            order_1.id
        )
        self.kitchen_simulator.process_new_orders()
        self.kitchen_simulator.order_controller.get_orders_by_status.assert_called_with(
            OrderStatus.NEW_ORDER.name,
            order_limit=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.NEW_ORDER],
        )
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_called_with(
            [order_1]
        )
        self.kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            OrderStatus.NEW_ORDER.name
        )
        # pylint: disable=W0212
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(
            arg_with_method_was_called[0].status, OrderStatus.CANCELLED.name
        )

    @mock.patch(
        "src.core.engine.processors.kitchen_simulator.compute_order_estimated_time",
        return_value=10,
    )
    def test_check_for_order_complete_successfully(
        self, mocked_compute_order_estimated_time
    ):

        kitchen_simulator = self.kitchen_simulator
        mongo_controller = kitchen_simulator.mongo_order_status_history_repository
        kitchen_simulator.assign_orders_to_available_chefs = mock.Mock()
        chef_1 = build_chef(chef_id=1)
        kitchen_simulator.chef_controller.get_by_id.return_value = chef_1
        product_ingredient_1 = build_product_ingredient(
            product_ingredient_id=1, quantity=2
        )
        kitchen_simulator.order_controller.get_order_ingredients_by_order_id.return_value = [
            product_ingredient_1
        ]

        order_1 = build_order(order_id=1, status=OrderStatus.IN_PROCESS)
        order_status_history = build_order_status_history(
            order_status_id=1,
            order_id=order_1.id,
            from_time=datetime.strptime(
                "2022-06-22 15:32:05.921969", "%Y-%m-%d %H:%M:%S.%f"
            ),
        )
        kitchen_simulator.order_manager.get_queue_from_status.return_value = 1
        kitchen_simulator.order_controller.get_by_id.return_value = order_1
        mongo_controller.get_last_status_history_by_order_id.return_value = (
            order_status_history
        )
        kitchen_simulator.process_orders_in_process()
        kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            OrderStatus.IN_PROCESS.name
        )
        kitchen_simulator.order_controller.get_by_id.assert_called_with(order_1.id)
        mongo_controller.get_last_status_history_by_order_id.assert_called_with(
            order_1.id
        )

        arg_with_method_was_call = (
            kitchen_simulator.order_manager.add_to_queue.mock_calls[0][1]
        )
        self.assertEqual(arg_with_method_was_call[0].status, OrderStatus.COMPLETED.name)
        mocked_compute_order_estimated_time.assert_called_with(
            [product_ingredient_1], chef_1
        )
