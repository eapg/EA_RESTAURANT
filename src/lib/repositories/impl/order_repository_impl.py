# This file has the order repository

from src.lib.repositories.order_repository import OrderRepository
from src.constants.order_status import OrderStatus


class OrderRepositoryImpl(OrderRepository):
    def __init__(
        self, order_detail_repository=None, product_ingredient_repository=None
    ):
        self._orders = {}
        self._current_id = 1
        self.order_detail_repository = order_detail_repository
        self.product_ingredient_repository = product_ingredient_repository

    def add(self, order):
        order.id = self._current_id
        self._orders[order.id] = order
        self._current_id += 1

    def get_by_id(self, order_id):
        return self._orders[order_id]

    def get_all(self):
        return list(self._orders.values())

    def delete_by_id(self, order_id):
        self._orders.pop(order_id)

    def update_by_id(self, order_id, order):
        current_order = self.get_by_id(order_id)
        current_order.order_details = order.order_details or current_order.order_details

    def get_orders_to_process(self):
        orders = self.get_all()

        orders_to_process = filter(
            lambda order: order.status == OrderStatus.NEW_ORDER, orders
        )
        return list(orders_to_process)

    def get_order_ingredients_by_order_id(self, order_id):

        order_details = self.order_detail_repository.get_by_order_id(order_id)
        product_ids = [order_detail.product_id for order_detail in order_details]
        filtered_product_ingredients = (
            self.product_ingredient_repository.get_product_ingredients_by_product_ids(
                product_ids
            )
        )
        return filtered_product_ingredients
