# This file has the inventory item repository

from src.main.repositories.generic_repository import GeneralRepository


class InventoryItemRepository(GeneralRepository):

    def __init__(self):
        self.__inventory_items = {}
        self.__current_id = 0

    def add(self, inventory_item):
        inventory_item.id = self.__current_id
        self.__inventory_items[inventory_item.id] = inventory_item
        self.__current_id += 1

    def get_by_id(self, inventory_item_id):
        return self.__inventory_items[inventory_item_id]

    def get_all(self):
        return self.__inventory_items.values()

    def delete_by_id(self, inventory_item_id):
        self.__inventory_items.pop(inventory_item_id)

    def update_by_id(self, inventory_item_id, inventory_item):
        current_inventory_item = self.get_by_id(inventory_item_id)
        current_inventory_item.item = inventory_item.item
        current_inventory_item.quantity = inventory_item.quantity

