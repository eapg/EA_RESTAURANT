# This file has the order_detail_order_detail repository

from src.lib.repositories.order_detail_repository import (
    OrderDetailRepository,
)


class OrderDetailRepositoryImpl(OrderDetailRepository):
    def __init__(self):
        self._order_details = {}
        self._current_id = 1

    def add(self, order_detail):
        order_detail.id = self._current_id
        self._order_details[order_detail.id] = order_detail
        self._current_id += 1

    def get_by_id(self, order_detail_id):
        return self._order_details[order_detail_id]

    def get_all(self):
        return list(self._order_details.values())

    def delete_by_id(self, order_detail_id):
        self._order_details.pop(order_detail_id)

    def update_by_id(self, order_detail_id, order_detail):
        current_order_detail = self.get_by_id(order_detail_id)
        current_order_detail.order_id = (
            order_detail.order_id or current_order_detail.order_id
        )
        current_order_detail.product_id = (
            order_detail.product_id or current_order_detail.product_id
        )
        current_order_detail.quantity = (
            order_detail.quantity or current_order_detail.quantity
        )

    def get_by_order_id(self, order_id):
        order_details = self.get_all()
        order_details_by_order_id = filter(
            (lambda order_detail: order_detail.order_id == order_id),
            order_details,
        )
        return list(order_details_by_order_id)
