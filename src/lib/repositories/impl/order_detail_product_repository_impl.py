# This file has the order_detail_order_detail_product repository

from src.lib.repositories.order_detail_product_repository import (
    OrderDetailProductRepository,
)


class OrderDetailProductRepositoryImpl(OrderDetailProductRepository):
    def __init__(self):
        self._order_detail_products = {}
        self._current_id = 1

    def add(self, order_detail_product):
        order_detail_product.id = self._current_id
        self._order_detail_products[order_detail_product.id] = order_detail_product
        self._current_id += 1

    def get_by_id(self, order_detail_product_id):
        return self._order_detail_products[order_detail_product_id]

    def get_all(self):
        return list(self._order_detail_products.values())

    def delete_by_id(self, order_detail_product_id):
        self._order_detail_products.pop(order_detail_product_id)

    def update_by_id(self, order_detail_product_id, order_detail_product):
        current_order_detail_product = self.get_by_id(order_detail_product_id)
        current_order_detail_product.order_detail_id = (
            order_detail_product.order_detail
            or current_order_detail_product.order_detail
        )
        current_order_detail_product.product = (
            order_detail_product.product or current_order_detail_product.product
        )
        current_order_detail_product.quantity = (
            order_detail_product.quantity or current_order_detail_product.quantity
        )
