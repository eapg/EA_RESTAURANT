# This file has the product repository

from src.main.repositories.generic_repository import GenericRepository


class ProductRepository(GenericRepository):

    def __init__(self):
        self.__products = {}
        self.__current_id = 0

    def add(self, product):
        product.id = self.__current_id
        self.__products[product.id] = product
        self.__current_id += 1

    def get_by_id(self, product_id):
        return self.__products[product_id]

    def get_all(self):
        return self.__products.values()

    def delete_by_id(self, product_id):
        self.__products.pop(product_id)

    def update_by_id(self, obj_id, obj):
        pass # pending for the future
