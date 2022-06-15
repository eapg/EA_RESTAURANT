from src.core.engine.processors.kitchen_simulator import KitchenSimulator
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.chef_fixture import build_chef
from src.tests.utils.fixtures.order_fixture import build_order
from src.constants.order_status import OrderStatus
from unittest import mock
import unittest


class KitchenSimulatorTest(unittest.TestCase):
    def setUp(self):
        self.app_engine_config = build_app_processor_config()
        self.kitchen_simulator = KitchenSimulator(self.app_engine_config)
        self.kitchen_simulator.order_manager = mock.Mock()
        self.kitchen_simulator.chef_controller = mock.Mock()
        self.kitchen_simulator.order_controller = mock.Mock()

    def test_assign_orders_to_available_chefs_when_order_is_valid(self):

        chef_1 = build_chef(chef_id=1)
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)

        self.kitchen_simulator.order_controller.get_orders_to_process.return_value = [
            order_1
        ]
        self.kitchen_simulator.chef_controller.get_available_chefs.return_value = [
            chef_1
        ]
        self.kitchen_simulator.order_controller.get_validated_orders_map.return_value = {
            1: True
        }
        self.kitchen_simulator.order_manager.get_queue_from_status.return_value = (
            order_1.id
        )
        self.kitchen_simulator.assign_orders_to_available_chefs()
        self.kitchen_simulator.order_controller.get_orders_to_process.assert_called_with(
            order_limit=1000
        )
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_called_with(
            [order_1]
        )

        self.kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            OrderStatus.NEW_ORDER
        )
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(arg_with_method_was_called[0].status, OrderStatus.IN_PROCESS)

    def test_assign_orders_to_available_chefs_when_order_is_not_valid(self):
        chef_1 = build_chef(chef_id=1)
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)

        self.kitchen_simulator.order_controller.get_orders_to_process.return_value = [
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
        self.kitchen_simulator.assign_orders_to_available_chefs()
        self.kitchen_simulator.order_controller.get_orders_to_process.assert_called_with(
            order_limit=1000
        )
        self.kitchen_simulator.order_controller.get_validated_orders_map.assert_called_with(
            [order_1]
        )
        self.kitchen_simulator.chef_controller.get_available_chefs.assert_called()
        self.kitchen_simulator.order_manager.get_queue_from_status.assert_called_with(
            OrderStatus.NEW_ORDER
        )
        arg_with_method_was_called = (
            self.kitchen_simulator.order_manager._mock_mock_calls[1][1]
        )
        self.assertEqual(arg_with_method_was_called[0].status, OrderStatus.CANCELLED)
