# This file has the order detail repository

from src.main.repositories.generic_repository import GeneralRepository


class OrderDetailRepository(GeneralRepository):

    def __init__(self):
        self.__orders_detail = {}
        self.__current_id = 0

    def add(self, order_detail):
        order_detail.id = self.__current_id
        self.__orders_detail[order_detail.id] = order_detail
        self.__current_id += 1

    def get_by_id(self, order_detail_id):
        return self.__orders_detail[order_detail_id]

    def get_all(self):
        return self.__orders_detail.values()

    def delete_by_id(self, order_detail_id):
        self.__orders_detail.pop(order_detail_id)

    def update_by_id(self, order_detail_id, order_detail):
        current_order_detail = self.get_by_id(order_detail_id)
        current_order_detail.order_product_list = order_detail.order_product_list


