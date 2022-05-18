# This file has the order_status_history repository

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
        current_order_status_history.order = (
            order_status_history.order or current_order_status_history.order
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
        order_status_histories_by_order_id = filter((lambda order_status_history: order_status_history.order.id == order_id), order_status_histories)
        return list(order_status_histories_by_order_id)
