# This file has the inventory ingredient repository impl

from src.lib.repositories.inventory_ingredient_repository import (
    InventoryIngredientRepository,
)


class InventoryIngredientRepositoryImpl(InventoryIngredientRepository):
    def __init__(self):

        self._inventory_ingredients = {}
        self._current_id = 1

    def add(self, inventory_ingredient):
        inventory_ingredient.id = self._current_id
        self._inventory_ingredients[inventory_ingredient.id] = inventory_ingredient
        self._current_id += 1

    def get_by_id(self, inventory_ingredient_id):
        return self._inventory_ingredients[inventory_ingredient_id]

    def get_all(self):
        return list(self._inventory_ingredients.values())

    def delete_by_id(self, inventory_ingredient_id):
        self._inventory_ingredients.pop(inventory_ingredient_id)

    def update_by_id(self, inventory_ingredient_id, inventory_ingredient):
        current_inventory_ingredient = self.get_by_id(inventory_ingredient_id)
        current_inventory_ingredient.ingredient = (
            inventory_ingredient.ingredient or current_inventory_ingredient.ingredient
        )
        current_inventory_ingredient.ingredient_quantity = (
            inventory_ingredient.ingredient_quantity
            or current_inventory_ingredient.ingredient_quantity
        )
