# This file has the ingredient repository
from datetime import datetime

from src.constants.audit import Status
from src.lib.repositories.ingredient_repository import IngredientRepository


class IngredientRepositoryImpl(IngredientRepository):
    def __init__(self):

        self._ingredients = {}
        self._current_id = 1

    def add(self, ingredient):
        ingredient.id = self._current_id
        ingredient.create_date = datetime.now()
        ingredient.update_by = ingredient.create_by
        ingredient.update_date = ingredient.create_date
        self._ingredients[ingredient.id] = ingredient
        self._current_id += 1

    def get_by_id(self, ingredient_id):
        ingredient_to_return = self._ingredients[ingredient_id]
        ingredient_filtered = list(
            filter(
                lambda ingredient: ingredient.entity_status == Status.ACTIVE,
                [ingredient_to_return],
            )
        )
        return ingredient_filtered[0]

    def get_all(self):
        ingredients = list(self._ingredients.values())
        products_filtered = list(
            filter(
                lambda ingredient: ingredient.entity_status == Status.ACTIVE,
                ingredients,
            )
        )
        return list(products_filtered)

    def delete_by_id(self, ingredient_id, ingredient):
        ingredient_to_be_delete = self.get_by_id(ingredient_id)
        ingredient_to_be_delete.entity_status = Status.DELETED
        ingredient_to_be_delete.update_date = datetime.now()
        ingredient_to_be_delete.update_by = ingredient.update_by
        self._update_by_id(
            ingredient_id, ingredient_to_be_delete, use_merge_with_existing=False
        )

    def update_by_id(self, ingredient_id, ingredient):
        self._update_by_id(ingredient_id, ingredient)

    def _update_by_id(self, ingredient_id, ingredient, use_merge_with_existing=True):
        current_ingredient = (
            self.get_by_id(ingredient_id) if use_merge_with_existing else ingredient
        )
        current_ingredient.name = ingredient.name or current_ingredient.name
        current_ingredient.description = (
            ingredient.description or current_ingredient.description
        )
        current_ingredient.update_date = datetime.now()
        current_ingredient.update_by = (
            ingredient.update_by or current_ingredient.update_by
        )
        current_ingredient.entity_status = (
            ingredient.entity_status or current_ingredient.entity_status
        )
