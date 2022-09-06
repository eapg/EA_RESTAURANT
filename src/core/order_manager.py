# order manager mechanism
import queue

from src.constants import order_status

ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP = {
    order_status.OrderStatus.NEW_ORDER: 1000,
    order_status.OrderStatus.CANCELLED: 1000,
    order_status.OrderStatus.IN_PROCESS: 1000,
    order_status.OrderStatus.COMPLETED: 1000,
}


class OrderManager:
    def __init__(self):
        self._order_status_to_order_queue_map = {
            order_status.OrderStatus.NEW_ORDER: queue.PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                    order_status.OrderStatus.NEW_ORDER
                ]
            ),
            order_status.OrderStatus.IN_PROCESS: queue.PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                    order_status.OrderStatus.IN_PROCESS
                ]
            ),
            order_status.OrderStatus.CANCELLED: queue.PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                    order_status.OrderStatus.CANCELLED
                ]
            ),
            order_status.OrderStatus.COMPLETED: queue.PriorityQueue(
                maxsize=ORDER_QUEUE_STATUS_TO_CHUNK_LIMIT_MAP[
                    order_status.OrderStatus.COMPLETED
                ]
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

        for status in [
            order_status.OrderStatus.COMPLETED,
            order_status.OrderStatus.CANCELLED,
        ]:
            if self.get_queue_size(status) > limit_value_before_clean:
                for _ in range(100):
                    deque_id = self.get_queue_from_status(status)
            else:
                self._order_status_to_order_queue_map[status].queue.clear()
