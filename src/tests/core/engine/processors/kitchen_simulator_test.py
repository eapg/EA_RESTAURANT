import unittest
from datetime import datetime
from unittest import mock

from src.constants import cooking_type
from src.constants import order_status
from src.core.engine.processors import kitchen_simulator
from src.tests.utils.fixtures import app_processor_config_fixture
from src.tests.utils.fixtures import chef_fixture
from src.tests.utils.fixtures import order_fixture
from src.tests.utils.fixtures import order_status_history_fixture
from src.tests.utils.fixtures import product_ingredient_fixture


class KitchenSimulatorTest(unittest.TestCase):
    def setUp(self):
        self.app_engine_config = (
            app_processor_config_fixture.build_app_processor_config()
        )
        self.kitchen_simulator = kitchen_simulator.KitchenSimulator(
            self.app_engine_config
        )
        self.kitchen_simulator.order_manager = mock.Mock()
        self.kitchen_simulator.chef_controller = mock.Mock()
        self.kitchen_simulator.order_controller = mock.Mock()
        self.kitchen_simulator.order_status_history_controller = mock.Mock()

    @mock.patch(
        "src.core.engine.processors.kitchen_simulator.order_util.compute_order_estimated_time"
    )
    def test_assign_orders_to_available_chefs_when_order_is_valid(
        self, mocked_order_estimated_time
    ):

        chef_1 = chef_fixture.build_chef(chef_id=1)
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.NEW_ORDER
        )

        self.kitchen_simulator.order_controller.get_orders_by_status.return_value = [
            order_1
        ]
        self.kitchen_simulator.order_controller.get_order_ingredients_by_order_id.return_value = [
            product_ingredient_fixture.build_product_ingredient(
                product_ingredient_id=1,
                quantity=1,
                ingredient_type=cooking_type.CookingType.FRYING,
            )
        ]
        self.kitchen_simulator.chef_controller.get_available_chefs.return_value = [
            chef_1
        ]
        self.kitchen_simulator.order_controller.get_validated_orders_map.return_value = {
            1: True
        }
        self.kitchen_simulator.order_manager.get_queue_size.return_value = 2
        self.kitchen_simulator.order_manager.get_queue_from_status.return_value = (
            order_1.id
        )
        self.kitchen_simulator.process_new_orders()
        self.kitchen_simulator.order_controller.get_orders_by_status.assert_called_with(
            order_status.OrderStatus.NEW_ORDER, order_limit=1000
        )
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_called_with(
            [order_1]
        )

        self.kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            order_status.OrderStatus.NEW_ORDER
        )
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(
            arg_with_method_was_called[0].status, order_status.OrderStatus.IN_PROCESS
        )
        mocked_order_estimated_time.asser_called_with(
            [
                product_ingredient_fixture.build_product_ingredient(
                    product_ingredient_id=1,
                    quantity=1,
                    ingredient_type=cooking_type.CookingType.FRYING,
                )
            ],
            chef_1,
        )
        self.kitchen_simulator.order_controller.reduce_order_ingredients_from_inventory.assert_called_with(
            order_1.id
        )

    def test_assign_orders_to_available_chefs_when_order_is_not_valid(self):
        chef_1 = chef_fixture.build_chef(chef_id=1)
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.NEW_ORDER
        )

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
            order_status.OrderStatus.NEW_ORDER, order_limit=1000
        )
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_called_with(
            [order_1]
        )
        self.kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            order_status.OrderStatus.NEW_ORDER
        )
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(
            arg_with_method_was_called[0].status, order_status.OrderStatus.CANCELLED
        )

    @mock.patch(
        "src.core.engine.processors.kitchen_simulator.order_util.compute_order_estimated_time",
        return_value=10,
    )
    def test_check_for_order_complete_successfully(
        self, mocked_compute_order_estimated_time
    ):
        self.kitchen_simulator.assign_orders_to_available_chefs = mock.Mock()
        self.kitchen_simulator.chef_controller.get_by_id.return_value = (
            chef_fixture.build_chef(chef_id=1)
        )
        self.kitchen_simulator.order_controller.get_order_ingredients_by_order_id.return_value = [
            product_ingredient_fixture.build_product_ingredient(
                product_ingredient_id=1,
                quantity=1,
                ingredient_type=cooking_type.CookingType.FRYING,
            )
        ]
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.IN_PROCESS
        )
        order_status_history = order_status_history_fixture.build_order_status_history(
            id=1,
            order_id=order_1.id,
            from_time=datetime.strptime(
                "2022-06-22 15:32:05.921969", "%Y-%m-%d %H:%M:%S.%f"
            ),
        )
        self.kitchen_simulator.order_manager.get_queue_from_status.return_value = 1
        self.kitchen_simulator.order_controller.get_by_id.return_value = order_1
        self.kitchen_simulator.order_status_history_controller.get_last_status_history_by_order_id.return_value = (
            order_status_history
        )
        self.kitchen_simulator.process_orders_in_process()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            order_status.OrderStatus.IN_PROCESS
        )
        self.kitchen_simulator.order_controller.get_by_id.assert_called_with(order_1.id)
        self.kitchen_simulator.order_status_history_controller.get_last_status_history_by_order_id.assert_called_with(
            order_1.id
        )

        arg_with_method_was_call = (
            self.kitchen_simulator.order_manager.add_to_queue.mock_calls[0][1]
        )
        self.assertEqual(
            arg_with_method_was_call[0].status, order_status.OrderStatus.COMPLETED
        )
        mocked_compute_order_estimated_time.assert_called_with(
            [
                product_ingredient_fixture.build_product_ingredient(
                    product_ingredient_id=1,
                    quantity=1,
                    ingredient_type=cooking_type.CookingType.FRYING,
                )
            ],
            chef_fixture.build_chef(chef_id=1),
        )
