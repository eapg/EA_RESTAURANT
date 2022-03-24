# This file has the order repository

from src.main.repositories.generic_repository import GeneralRepository


class OrderRepository(GeneralRepository):

    def __init__(self):
        self.__orders = {}
        self.__current_id = 0

    def add(self, order):
        order.id = self.__current_id
        self.__orders[order.id] = order
        self.__current_id += 1

    def get_by_id(self, order_id):
        return self.__orders[order_id]

    def get_all(self):
        return self.__orders.values()

    def delete_by_id(self, order_id):
        self.__orders.pop(order_id)

    def update_by_id(self, order_id, order):
        current_order = self.get_by_id(order_id)
        current_order.order_details = order.order_details


