# order manager mechanism
import queue
from queue import PriorityQueue

from src.constants.order_status import OrderStatus

ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP = {
    OrderStatus.NEW_ORDER: 1000,
    OrderStatus.CANCELLED: 1000,
    OrderStatus.IN_PROCESS: 1000,
    OrderStatus.COMPLETED: 1000,
}


class OrderManager:
    def __init__(self):
        self._order_status_to_order_queue_map = {
            OrderStatus.NEW_ORDER.name: PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.NEW_ORDER]
            ),
            OrderStatus.IN_PROCESS.name: PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.IN_PROCESS]
            ),
            OrderStatus.CANCELLED.name: PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.CANCELLED]
            ),
            OrderStatus.COMPLETED.name: PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[OrderStatus.COMPLETED]
            ),
        }

    def add_to_queue(self, order):
        if self.get_queue_size(order.status) == 1000:
            raise OverflowError("Queue Full")
        self._order_status_to_order_queue_map[order.status].put(order.id, order.id)

    def get_queue_from_status(self, order_status):
        try:
            return self._order_status_to_order_queue_map[order_status].get_nowait()
        except queue.Empty:
            return None

    def get_queue_size(self, order_status):
        return self._order_status_to_order_queue_map[order_status].qsize()

    def is_order_queue_empty(self, order_status):
        return self._order_status_to_order_queue_map[order_status].empty()

    def clean_queues_with_full_storage(self, limit_value_before_clean=500):

        for status in [OrderStatus.COMPLETED.name, OrderStatus.CANCELLED.name]:
            if self.get_queue_size(status) > limit_value_before_clean:
                for _ in range(100):
                    deque_id = self.get_queue_from_status(status)
            else:
                self._order_status_to_order_queue_map[status].queue.clear()
