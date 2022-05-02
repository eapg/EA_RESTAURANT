# This file has the inventory repository

from src.lib.repositories.inventory_repository import InventoryRepository


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self, inventory_ingredient_repository):
        self._inventories = {}
        self.inventory_ingredient_repository = inventory_ingredient_repository
        self._current_id = 1


    def add(self, inventory):
        inventory.id = self._current_id
        self._inventories[inventory.id] = inventory
        self._current_id += 1

    def get_by_id(self, inventory_id):
        return self._inventories[inventory_id]

    def get_all(self):
        return list(self._inventories.values())

    def delete_by_id(self, inventory_id):
        self._inventories.pop(inventory_id)

    def update_by_id(self, inventory_id, inventory):
        current_inventory = self.get_by_id(inventory_id)
        current_inventory.inventory_ingredients = (
            inventory.inventory_ingredients or current_inventory.inventory_ingredients
        )

    def inventory_ingredient_availability(
        self, inventory_id, ingredient_id, availability
    ):

        ingredients_inventory = self.get_by_id(inventory_id)
        inventory_ingredient_id = ingredients_inventory.inventory_ingredients[
            ingredient_id
        ].id
        inventory_ingredient = self.inventory_ingredient_repository.get_by_id(
            inventory_ingredient_id
        )

        if inventory_ingredient.ingredient_quantity >= availability:
            return True
        else:
            return False
