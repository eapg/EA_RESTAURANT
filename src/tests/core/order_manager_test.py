import unittest

from src.constants import order_status
from src.core import order_manager
from src.tests.utils.fixtures import order_fixture


class OrderManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_manager = order_manager.OrderManager()

    def test_get_from_order_storage(self):
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.NEW_ORDER
        )
        order_2 = order_fixture.build_order(
            order_id=2, status=order_status.OrderStatus.NEW_ORDER
        )
        order_3 = order_fixture.build_order(
            order_id=3, status=order_status.OrderStatus.NEW_ORDER
        )

        self.order_manager.add_to_queue(order_3)
        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_id_pulled_with_id_priority = self.order_manager.get_queue_from_status(
            order_status.OrderStatus.NEW_ORDER
        )
        self.assertEqual(order_id_pulled_with_id_priority, order_1.id)

    def test_get_queue_size(self):
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.NEW_ORDER
        )
        order_2 = order_fixture.build_order(
            order_id=2, status=order_status.OrderStatus.NEW_ORDER
        )

        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_placed_storage_size = self.order_manager.get_queue_size(
            order_status.OrderStatus.NEW_ORDER
        )
        self.assertEqual(order_placed_storage_size, 2)

    def test_get_queue_status_empty(self):
        queue_status = self.order_manager.is_order_queue_empty(
            order_status.OrderStatus.NEW_ORDER
        )
        self.assertTrue(queue_status)

    def test_clean_queues_with_full_storage(self):
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.COMPLETED
        )
        order_2 = order_fixture.build_order(
            order_id=2, status=order_status.OrderStatus.COMPLETED
        )
        order_3 = order_fixture.build_order(
            order_id=3, status=order_status.OrderStatus.COMPLETED
        )

        order_manager_instance = order_manager.OrderManager()
        order_manager_instance.add_to_queue(order_1)
        order_manager_instance.add_to_queue(order_2)
        order_manager_instance.add_to_queue(order_3)
        order_manager_instance.clean_queues_with_full_storage(
            limit_value_before_clean=2
        )
        completed_queue_size_after_clean = order_manager_instance.get_queue_size(
            order_status.OrderStatus.COMPLETED
        )
        self.assertEqual(completed_queue_size_after_clean, 0)
