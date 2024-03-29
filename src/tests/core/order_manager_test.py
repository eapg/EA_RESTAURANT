from src.constants.order_status import OrderStatus
from src.core.order_manager import OrderManager
from src.tests.base_env_config_test import BaseEnvConfigTest
from src.tests.utils.fixtures.mapping_orm_fixtures import build_order


class OrderManagerTestCase(BaseEnvConfigTest):
    def setUp(self):
        super().setUp()
        self.order_manager = OrderManager()

    def test_get_from_order_storage(self):
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER.name)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER.name)
        order_3 = build_order(order_id=3, status=OrderStatus.NEW_ORDER.name)

        self.order_manager.add_to_queue(order_3)
        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_id_pulled_with_id_priority = self.order_manager.get_queue_from_status(
            OrderStatus.NEW_ORDER.name
        )
        self.assertEqual(order_id_pulled_with_id_priority, order_1.id)

    def test_get_queue_size(self):
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER.name)
        order_2 = build_order(order_id=2, status=OrderStatus.NEW_ORDER.name)

        self.order_manager.add_to_queue(order_1)
        self.order_manager.add_to_queue(order_2)

        order_placed_storage_size = self.order_manager.get_queue_size(
            OrderStatus.NEW_ORDER.name
        )
        self.assertEqual(order_placed_storage_size, 2)

    def test_get_queue_status_empty(self):
        queue_status = self.order_manager.is_order_queue_empty(
            OrderStatus.NEW_ORDER.name
        )
        self.assertTrue(queue_status)

    def test_clean_queues_with_full_storage(self):
        order_1 = build_order(order_id=1, status=OrderStatus.COMPLETED.name)
        order_2 = build_order(order_id=2, status=OrderStatus.COMPLETED.name)
        order_3 = build_order(order_id=3, status=OrderStatus.COMPLETED.name)

        order_manager = OrderManager()
        order_manager.add_to_queue(order_1)
        order_manager.add_to_queue(order_2)
        order_manager.add_to_queue(order_3)
        order_manager.clean_queues_with_full_storage(limit_value_before_clean=2)
        completed_queue_size_after_clean = order_manager.get_queue_size(
            OrderStatus.COMPLETED.name
        )
        self.assertEqual(completed_queue_size_after_clean, 0)
