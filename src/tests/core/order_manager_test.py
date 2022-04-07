import unittest
from src.core.order_manager import OrderManager
from src.tests.utils.fixtures.order_fixture import build_order
from src.constants.order_status import OrderStatus


class OrderManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_manager = OrderManager()

    def test_get_from_order_storage(self):
        order_1 = build_order(order_status=OrderStatus.ORDER_PLACED)
        order_2 = build_order(order_status=OrderStatus.ORDER_PLACED)
        order_3 = build_order(order_status=OrderStatus.ORDER_PLACED)

        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)
        self.order_manager.add_to_queue(order_3)

        order_pulled = self.order_manager.get_queue_from_status("order_placed")
        self.assertEqual(order_pulled, order_1)

    def test_get_queue_size(self):
        order_1 = build_order(order_status=OrderStatus.ORDER_PLACED)
        order_2 = build_order(order_status=OrderStatus.ORDER_PLACED)

        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_placed_storage_size = self.order_manager.get_queue_size("order_placed")
        self.assertEqual(order_placed_storage_size, 2)

    def test_get_queue_status_empty(self):
        queue_status = self.order_manager.is_order_queue_empty("order_placed")
        self.assertTrue(queue_status)
