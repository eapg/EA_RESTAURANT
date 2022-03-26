# This file has the ingredient repository

from src.lib.repositories.ingredient_repository import IngredientRepository


class IngredientRepositoryImpl(IngredientRepository):
    def __init__(self):

        self._ingredients = {}
        self._current_id = 1

    def add(self, ingredient):
        ingredient.id = self._current_id
        self._ingredients[ingredient.id] = ingredient
        self._current_id += 1

    def get_by_id(self, ingredient_id):
        return self._ingredients[ingredient_id]

    def get_all(self):
        return list(self._ingredients.values())

    def delete_by_id(self, ingredient_id):
        self._ingredients.pop(ingredient_id)

    def update_by_id(self, ingredient_id, ingredient):
        current_ingredient = self.get_by_id(ingredient_id)
        current_ingredient.name = ingredient.name or current_ingredient.name
        current_ingredient.description = (
            ingredient.description or current_ingredient.description
        )
