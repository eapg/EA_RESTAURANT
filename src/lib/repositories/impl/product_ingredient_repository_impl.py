# This file has the product_ingredient repository

from src.lib.repositories.product_ingredient_repository import (
    ProductIngredientRepository,
)


class ProductIngredientRepositoryImpl(ProductIngredientRepository):
    def __init__(self):
        self._product_ingredients = {}
        self._current_id = 1

    def add(self, product_ingredient):
        product_ingredient.id = self._current_id
        self._product_ingredients[product_ingredient.id] = product_ingredient
        self._current_id += 1

    def get_by_id(self, product_ingredient_id):
        return self._product_ingredients[product_ingredient_id]

    def get_all(self):
        return list(self._product_ingredients.values())

    def delete_by_id(self, product_ingredient_id):
        self._product_ingredients.pop(product_ingredient_id)

    def update_by_id(self, product_ingredient_id, product_ingredient):
        current_product_ingredient = self.get_by_id(product_ingredient_id)
        current_product_ingredient.product = (
            product_ingredient.product or current_product_ingredient.product
        )
        current_product_ingredient.ingredient = (
            product_ingredient.ingredient or current_product_ingredient.ingredient
        )
        current_product_ingredient.quantity = (
            product_ingredient.quantity or current_product_ingredient.quantity
        )
