import unittest
from src.core.order_manager import OrderManager
from src.tests.utils.fixtures.order_fixture import build_order
from src.constants.order_status import OrderStatus


class OrderManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_manager = OrderManager()

    def test_get_from_order_storage(self):
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER)
        order_3 = build_order(order_id=3, status=OrderStatus.NEW_ORDER)

        self.order_manager.add_to_queue(order_3)
        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_id_pulled_with_id_priority = self.order_manager.get_queue_from_status(OrderStatus.NEW_ORDER)
        self.assertEqual(order_id_pulled_with_id_priority, order_1.id)

    def test_get_queue_size(self):
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER)

        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_placed_storage_size = self.order_manager.get_queue_size(OrderStatus.NEW_ORDER)
        self.assertEqual(order_placed_storage_size, 2)

    def test_get_queue_status_empty(self):
        queue_status = self.order_manager.is_order_queue_empty(OrderStatus.NEW_ORDER)
        self.assertTrue(queue_status)
