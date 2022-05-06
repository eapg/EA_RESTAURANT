import unittest
from unittest import mock

from src.api.controllers.order_controller import OrderController
from src.tests.utils.fixtures.order_fixture import build_order, build_orders


class OrderRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = mock.Mock()
        self.order_controller = OrderController(self.order_repository)

    def test_add_order_successfully(self):
        order = build_order()

        self.order_controller.add(order)

        self.order_repository.add.assert_called_with(order)

    def test_get_order_successfully(self):
        order = build_order()

        self.order_repository.get_by_id.return_value = order

        expected_order = self.order_controller.get_by_id(order.id)

        self.order_repository.get_by_id.assert_called_with(order.id)
        self.assertEqual(expected_order.id, order.id)

    def test_get_all_orders_successfully(self):
        orders = build_orders(count=3)

        self.order_repository.get_all.return_value = orders

        expected_orders = self.order_controller.get_all()

        self.order_repository.get_all.assert_called()
        self.assertEqual(expected_orders, orders)
        self.assertEqual(len(expected_orders), 3)

    def test_delete_an_order_successfully(self):
        self.order_controller.delete_by_id(2)

        self.order_repository.delete_by_id.assert_called_with(2)

    def test_update_an_order_successfully(self):
        order = build_order()

        self.order_controller.update_by_id(1, order)

        self.order_repository.update_by_id.assert_called_with(1, order)

    def test_get_orders_to_process_successfully(self):

        orders_to_process = self.order_controller.get_orders_to_process()
        self.order_repository.get_orders_to_process.assert_called()
