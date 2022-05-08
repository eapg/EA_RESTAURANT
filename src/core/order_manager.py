# order manager mechanism

from queue import Queue


class OrderManager:
    def __init__(self):
        self._order_status_to_order_queue_map = {
            "order_placed": Queue(maxsize=0),
            "in_process": Queue(maxsize=0),
            "cancelled": Queue(maxsize=0),
            "completed": Queue(maxsize=0),
        }

    def add_to_queue(self, order):
        self._order_status_to_order_queue_map[order.status.value].put(order.id)

    def get_queue_from_status(self, order_status):
        return self._order_status_to_order_queue_map[order_status].get()

    def get_queue_size(self, order_status):
        return self._order_status_to_order_queue_map[order_status].qsize()

    def is_order_queue_empty(self, order_status):
        return self._order_status_to_order_queue_map[order_status].empty()
