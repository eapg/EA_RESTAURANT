# This file has the inventory repository

from src.main.repositories.generic_repository import GeneralRepository


class InventoryRepository(GeneralRepository):

    def __init__(self):
        self.__inventories = {}
        self.__current_id = 0

    def add(self, inventory):
        inventory.id = self.__current_id
        self.__inventories[inventory.id] = inventory
        self.__current_id += 1

    def get_by_id(self, inventory_id):
        return self.__inventories[inventory_id]

    def get_all(self):
        return self.__inventories.values()

    def delete_by_id(self, inventory_id):
        self.__inventories.pop(inventory_id)

    def update_by_id(self, inventory_id, inventory):
        current_inventory = self.get_by_id(inventory_id)
        current_inventory.inventory_item_list = inventory.inventory_item_list

