# This file has the product_ingredient repository
from datetime import datetime

from src.constants.audit import Status
from src.lib.repositories.product_ingredient_repository import \
    ProductIngredientRepository


class ProductIngredientRepositoryImpl(ProductIngredientRepository):
    def __init__(self):
        self._product_ingredients = {}
        self._current_id = 1

    def add(self, product_ingredient):
        product_ingredient.id = self._current_id
        product_ingredient.created_date = datetime.now()
        product_ingredient.updated_by = product_ingredient.created_by
        product_ingredient.updated_date = product_ingredient.created_date
        self._product_ingredients[product_ingredient.id] = product_ingredient
        self._current_id += 1

    def get_by_id(self, product_ingredient_id):
        product_ingredient_to_return = self._product_ingredients[product_ingredient_id]
        product_ingredient_filtered = list(
            filter(
                lambda product_ingredient: product_ingredient.entity_status
                == Status.ACTIVE,
                [product_ingredient_to_return],
            )
        )
        return product_ingredient_filtered[0]

    def get_all(self):
        product_ingredients = list(self._product_ingredients.values())
        product_ingredients_filtered = filter(
            lambda product_ingredient: product_ingredient.entity_status
            == Status.ACTIVE,
            product_ingredients,
        )
        return list(product_ingredients_filtered)

    def delete_by_id(self, product_ingredient_id, product_ingredient):
        product_ingredient_to_be_delete = self.get_by_id(product_ingredient_id)
        product_ingredient_to_be_delete.entity_status = Status.DELETED
        product_ingredient_to_be_delete.updated_date = datetime.now()
        product_ingredient_to_be_delete.updated_by = product_ingredient.updated_by
        self._update_by_id(
            product_ingredient_id,
            product_ingredient_to_be_delete,
            use_merge_with_existing=False,
        )

    def update_by_id(self, product_ingredient_id, product_ingredient):
        self._update_by_id(product_ingredient_id, product_ingredient)

    def _update_by_id(
        self, product_ingredient_id, product_ingredient, use_merge_with_existing=True
    ):
        current_product_ingredient = (
            self.get_by_id(product_ingredient_id)
            if use_merge_with_existing
            else product_ingredient
        )
        current_product_ingredient.product_id = (
            product_ingredient.product_id or current_product_ingredient.product_id
        )
        current_product_ingredient.ingredient_id = (
            product_ingredient.ingredient_id or current_product_ingredient.ingredient_id
        )
        current_product_ingredient.quantity = (
            product_ingredient.quantity or current_product_ingredient.quantity
        )
        current_product_ingredient.ingredient_type = (
            product_ingredient.ingredient_type
            or current_product_ingredient.ingredient_type
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
