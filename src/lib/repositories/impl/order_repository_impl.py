# This file has the order repository
from functools import reduce
from datetime import datetime

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.repositories.order_repository import OrderRepository
from src.utils.order_util import (
    array_chef_to_chef_assigned_orders_map_reducer,
    setup_validated_orders_map,
)


class OrderRepositoryImpl(OrderRepository):
    def __init__(
        self,
        order_detail_repository=None,
        product_ingredient_repository=None,
        inventory_ingredient_repository=None,
    ):
        self._orders = {}
        self._current_id = 1
        self.order_detail_repository = order_detail_repository
        self.product_ingredient_repository = product_ingredient_repository
        self.inventory_ingredient_repository = inventory_ingredient_repository

    def add(self, order):
        order.id = self._current_id
        order.create_date = datetime.now()
        order.update_by = order.create_by
        order.update_date = order.create_date
        self._orders[order.id] = order
        self._current_id += 1

    def get_by_id(self, order_id):
        order_to_return = self._orders[order_id]
        order_filtered = list(
            filter(
                lambda order: order.entity_status == Status.ACTIVE,
                [order_to_return],
            )
        )
        return order_filtered[0]

    def get_all(self):
        orders = list(self._orders.values())
        orders_filtered = filter(
            lambda order: order.entity_status == Status.ACTIVE, orders
        )
        return list(orders_filtered)

    def delete_by_id(self, order_id, order):
        order_to_be_delete = self.get_by_id(order_id)
        order_to_be_delete.entity_status = Status.DELETED
        order_to_be_delete.update_date = datetime.now()
        order_to_be_delete.update_by = order.update_by
        self._update_by_id(order_id, order_to_be_delete, use_merge_with_existing=False)

    def update_by_id(self, order_id, order):
        self._update_by_id(order_id, order)

    def _update_by_id(self, order_id, order, use_merge_with_existing=True):
        current_order = self.get_by_id(order_id) if use_merge_with_existing else order
        current_order.status = order.status or current_order.status
        current_order.assigned_chef_id = (
            order.assigned_chef_id or current_order.assigned_chef_id
        )
        current_order.update_date = datetime.now()
        current_order.update_by = order.update_by or current_order.update_by
        current_order.entity_status = order.entity_status or current_order.entity_status

    def get_orders_by_status(self, order_status, order_limit=None):
        orders = self.get_all()
        orders_by_status = filter(lambda order: order.status == order_status, orders)
        return (list(orders_by_status))[0:order_limit]

    def get_chefs_with_assigned_orders(self, chef_ids):

        orders = self.get_orders_by_status(OrderStatus.IN_PROCESS)
        chefs_with_assigned_orders_map = reduce(
            lambda assigned_chef_result, chef_id: array_chef_to_chef_assigned_orders_map_reducer(
                assigned_chef_result, chef_id, orders
            ),
            chef_ids,
            {},
        )

        return chefs_with_assigned_orders_map

    def get_order_ingredients_by_order_id(self, order_id):

        order_details = self.order_detail_repository.get_by_order_id(order_id)
        product_ids = [order_detail.product_id for order_detail in order_details]
        filtered_product_ingredients = (
            self.product_ingredient_repository.get_product_ingredients_by_product_ids(
                product_ids
            )
        )
        return filtered_product_ingredients

    def get_validated_orders_map(self, orders_to_process):
        reduce_validated_orders_map = setup_validated_orders_map(
            self.inventory_ingredient_repository.get_final_product_qty_by_product_ids,
            self.order_detail_repository.get_by_order_id,
        )
        validated_orders_map = reduce_validated_orders_map(orders_to_process)
        return validated_orders_map

    def reduce_order_ingredients_from_inventory(self, order_id):

        order_product_ingredients = self.get_order_ingredients_by_order_id(order_id)

        for product_ingredient in order_product_ingredients:

            inventory_ingredient = (
                self.inventory_ingredient_repository.get_by_ingredient_id(
                    product_ingredient.ingredient_id
                )
            )
            inventory_ingredient[0].ingredient_quantity = (
                inventory_ingredient[0].ingredient_quantity
                - product_ingredient.quantity
            )
            self.inventory_ingredient_repository.update_by_id(
                inventory_ingredient[0].id, inventory_ingredient[0]
            )
