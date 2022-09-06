# This file has the order_status_history repository
from datetime import datetime

from src.constants import audit
from src.lib.entities import order_status_history
from src.lib.repositories import order_status_history_repository


class OrderStatusHistoryRepositoryImpl(
    order_status_history_repository.OrderStatusHistoryRepository
):
    def __init__(self):
        self._order_status_histories = {}
        self._current_id = 1

    def add(self, order_status_history):
        order_status_history.id = self._current_id
        order_status_history.created_date = datetime.now()
        order_status_history.updated_by = order_status_history.created_by
        order_status_history.updated_date = order_status_history.created_date
        self._order_status_histories[order_status_history.id] = order_status_history
        self._current_id += 1

    def get_by_id(self, order_status_history_id):
        order_status_history_to_return = self._order_status_histories[
            order_status_history_id
        ]
        order_status_history_filtered = list(
            filter(
                lambda order_status_history: order_status_history.entity_status
                == audit.Status.ACTIVE,
                [order_status_history_to_return],
            )
        )
        return order_status_history_filtered[0]

    def get_all(self):
        order_status_histories = list(self._order_status_histories.values())
        order_status_histories_filtered = filter(
            lambda order_status_history: order_status_history.entity_status
            == audit.Status.ACTIVE,
            order_status_histories,
        )
        return list(order_status_histories_filtered)

    def delete_by_id(self, order_status_history_id, order_status_history):
        order_status_history_to_be_delete = self.get_by_id(order_status_history_id)
        order_status_history_to_be_delete.entity_status = audit.Status.DELETED
        order_status_history_to_be_delete.updated_date = datetime.now()
        order_status_history_to_be_delete.updated_by = order_status_history.updated_by
        self._update_by_id(
            order_status_history_id,
            order_status_history_to_be_delete,
            use_merge_with_existing=False,
        )

    def update_by_id(self, order_status_history_id, order_status_history):
        self._update_by_id(order_status_history_id, order_status_history)

    def _update_by_id(
        self,
        order_status_history_id,
        order_status_history,
        use_merge_with_existing=True,
    ):
        current_order_status_history = (
            self.get_by_id(order_status_history_id)
            if use_merge_with_existing
            else order_status_history
        )
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
        current_order_status_history.updated_date = datetime.now()
        current_order_status_history.updated_by = (
            order_status_history.updated_by or current_order_status_history.updated_by
        )
        current_order_status_history.entity_status = (
            order_status_history.entity_status
            or current_order_status_history.entity_status
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

        new_status_history = order_status_history.OrderStatusHistory()
        new_status_history.from_status = new_status
        new_status_history.from_time = datetime.now()
        new_status_history.entity_status = audit.Status.ACTIVE
        new_status_history.order_id = order_id
        self.add(new_status_history)
