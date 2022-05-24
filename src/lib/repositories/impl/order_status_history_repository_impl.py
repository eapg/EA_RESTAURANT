# This file has the order_status_history repository
from datetime import datetime

from src.lib.entities.order_status_history import OrderStatusHistory
from src.lib.repositories.order_status_history_repository import (
    OrderStatusHistoryRepository,
)


class OrderStatusHistoryRepositoryImpl(OrderStatusHistoryRepository):
    def __init__(self):
        self._order_status_histories = {}
        self._current_id = 1

    def add(self, order_status_history):
        order_status_history.id = self._current_id
        self._order_status_histories[order_status_history.id] = order_status_history
        self._current_id += 1

    def get_by_id(self, order_status_history_id):
        return self._order_status_histories[order_status_history_id]

    def get_all(self):
        return list(self._order_status_histories.values())

    def delete_by_id(self, order_status_history_id):
        self._order_status_histories.pop(order_status_history_id)

    def update_by_id(self, order_status_history_id, order_status_history):
        current_order_status_history = self.get_by_id(order_status_history_id)
        current_order_status_history.order_id = (
            order_status_history.order_id or current_order_status_history.order_id
        )
        current_order_status_history.from_time = (
            order_status_history.from_time or current_order_status_history.from_time
        )
        current_order_status_history.to_time = (
            order_status_history.to_time or current_order_status_history.to_time
        )
        current_order_status_history.from_status = (
            order_status_history.from_status or current_order_status_history.from_status
        )
        current_order_status_history.to_status = (
            order_status_history.to_status or current_order_status_history.to_status
        )

    def get_by_order_id(self, order_id):
        order_status_histories = self.get_all()
        order_status_histories_by_order_id = filter(
            (lambda order_status_history: order_status_history.order_id == order_id),
            order_status_histories,
        )
        return list(order_status_histories_by_order_id)

    def get_last_status_history_by_order_id(self, order_id):
        order_status_histories = self.get_by_order_id(order_id)
        order_status_history_id = 0
        last_order_status_history = None
        for order_status_history in order_status_histories:

            if order_status_history.id > order_status_history_id:
                order_status_history_id = order_status_history.id
                last_order_status_history = order_status_history

        return last_order_status_history

    def set_next_status_history_by_order_id(self, order_id, new_status):
        last_order_status_history = self.get_last_status_history_by_order_id(order_id)

        if last_order_status_history:
            last_order_status_history.to_status = new_status
            last_order_status_history.to_time = datetime.now()
            self.update_by_id(last_order_status_history.id, last_order_status_history)

        new_status_history = OrderStatusHistory()
        new_status_history.from_status = new_status
        new_status_history.from_time = datetime.now()
        new_status_history.order_id = order_id
        self.add(new_status_history)
