# order manager mechanism

from queue import Queue
from src.constants.order_status import OrderStatus


class OrderManager:
    def __init__(self):
        self._order_status_to_order_queue_map = {
            OrderStatus.NEW_ORDER: Queue(maxsize=1000),
            OrderStatus.IN_PROCESS: Queue(maxsize=1000),
            OrderStatus.CANCELLED: Queue(maxsize=1000),
            OrderStatus.COMPLETED: Queue(maxsize=1000),
        }

    def add_to_queue(self, order):
        if self.get_queue_size(order.status) == 1000:
            raise OverflowError("Queue Full")
        self._order_status_to_order_queue_map[order.status].put(order.id)

    def get_queue_from_status(self, order_status):
        return self._order_status_to_order_queue_map[order_status].get()

    def get_queue_size(self, order_status):
        return self._order_status_to_order_queue_map[order_status].qsize()

    def is_order_queue_empty(self, order_status):
        return self._order_status_to_order_queue_map[order_status].empty()
