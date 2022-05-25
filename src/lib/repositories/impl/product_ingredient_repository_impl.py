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
        current_product_ingredient.product_id = (
            product_ingredient.product_id or current_product_ingredient.product_id
        )
        current_product_ingredient.ingredient_id = (
            product_ingredient.ingredient_id or current_product_ingredient.ingredient_id
        )
        current_product_ingredient.quantity = (
            product_ingredient.quantity or current_product_ingredient.quantity
        )

    def get_by_product_id(self, product_id):
        product_ingredients = self.get_all()
        product_ingredients_of_product = filter(
            (lambda product_ingredient: product_id == product_ingredient.product_id),
            product_ingredients,
        )
        return list(product_ingredients_of_product)

    def get_product_ingredients_by_product_ids(self, product_ids):

        product_ingredients = self.get_all()
        filtered_product_ingredients = filter(
            (lambda product_ingredient: product_ingredient.product_id in product_ids),
            product_ingredients,
        )

        return list(filtered_product_ingredients)
