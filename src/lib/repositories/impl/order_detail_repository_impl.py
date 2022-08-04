# This file has the order_detail_order_detail repository
from datetime import datetime

from src.constants.audit import Status
from src.lib.repositories.order_detail_repository import OrderDetailRepository


class OrderDetailRepositoryImpl(OrderDetailRepository):
    def __init__(self):
        self._order_details = {}
        self._current_id = 1

    def add(self, order_detail):
        order_detail.id = self._current_id
        order_detail.create_date = datetime.now()
        order_detail.update_by = order_detail.create_by
        order_detail.update_date = order_detail.create_date
        self._order_details[order_detail.id] = order_detail
        self._current_id += 1

    def get_by_id(self, order_detail_id):
        order_detail_to_return = self._order_details[order_detail_id]
        order_detail_filtered = list(
            filter(
                lambda order_detail: order_detail.entity_status == Status.ACTIVE,
                [order_detail_to_return],
            )
        )
        return order_detail_filtered[0]

    def get_all(self):
        order_details = list(self._order_details.values())
        order_details_filtered = filter(
            lambda order_detail: order_detail.entity_status == Status.ACTIVE,
            order_details,
        )
        return list(order_details_filtered)

    def delete_by_id(self, order_detail_id, order_detail):
        order_detail_to_be_delete = self.get_by_id(order_detail_id)
        order_detail_to_be_delete.entity_status = Status.DELETED
        order_detail_to_be_delete.update_date = datetime.now()
        order_detail_to_be_delete.update_by = order_detail.update_by
        self._update_by_id(
            order_detail, order_detail_to_be_delete, use_merge_with_existing=False
        )

    def update_by_id(self, order_detail_id, order_detail):
        self._update_by_id(order_detail_id, order_detail)

    def _update_by_id(
        self, order_detail_id, order_detail, use_merge_with_existing=True
    ):
        current_order_detail = (
            self.get_by_id(order_detail_id) if use_merge_with_existing else order_detail
        )
        current_order_detail.order_id = (
            order_detail.order_id or current_order_detail.order_id
        )
        current_order_detail.product_id = (
            order_detail.product_id or current_order_detail.product_id
        )
        current_order_detail.quantity = (
            order_detail.quantity or current_order_detail.quantity
        )
        current_order_detail.update_date = datetime.now()
        current_order_detail.update_by = (
            order_detail.update_by or current_order_detail.update_by
        )
        current_order_detail.entity_status = (
            order_detail.entity_status or current_order_detail.entity_status
        )

    def get_by_order_id(self, order_id):
        order_details = self.get_all()
        order_details_by_order_id = filter(
            (lambda order_detail: order_detail.order_id == order_id),
            order_details,
        )
        return list(order_details_by_order_id)
