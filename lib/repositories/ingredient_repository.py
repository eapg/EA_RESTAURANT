# This file has the item repository

from lib.repositories.generic_repository import GenericRepository


class IngredientRepository(GenericRepository):

    def __init__(self):
        self.__items = {}
        self.__current_id = 0

    def add(self, item):
        item.id = self.__current_id
        self.__items[item.id] = item
        self.__current_id += 1

    def get_by_id(self, item_id):
        return self.__items[item_id]

    def get_all(self):
        return self.__items.values()

    def delete_by_id(self, item_id):
        self.__items.pop(item_id)

    def update_by_id(self, item_id, item):
        current_item = self.get_by_id(item_id)
        current_item.name = item.name


