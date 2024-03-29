# Interface for the repositories through Abstract method
from abc import ABCMeta

from src.lib.repositories.generic_repository import GenericRepository


class OrderRepository(GenericRepository, metaclass=ABCMeta):
    @staticmethod
    def get_orders_by_status(order_status, order_limit=None):
        pass

    @staticmethod
    def get_chefs_with_assigned_orders(chef_ids):
        pass

    @staticmethod
    def get_order_ingredients_by_order_id(order_id):
        pass

    @staticmethod
    def get_validated_orders_map(orders_to_process):
        pass

    @staticmethod
    def reduce_order_ingredients_from_inventory(order_id):
        pass
