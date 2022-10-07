# This file has the inventory ingredient repository impl_v2
from datetime import datetime

from src.constants.audit import Status
from src.lib.repositories.inventory_ingredient_repository import \
    InventoryIngredientRepository
from src.utils.inventory_ingredient_util import \
    setup_products_qty_array_to_final_products_qty_map


class InventoryIngredientRepositoryImpl(InventoryIngredientRepository):
    def __init__(self, product_ingredient_repository=None):

        self._inventory_ingredients = {}
        self._current_id = 1
        self.product_ingredient_repository = product_ingredient_repository

    def add(self, inventory_ingredient):
        inventory_ingredient.id = self._current_id
        inventory_ingredient.created_date = datetime.now()
        inventory_ingredient.updated_by = inventory_ingredient.created_by
        inventory_ingredient.updated_date = inventory_ingredient.created_date
        self._inventory_ingredients[inventory_ingredient.id] = inventory_ingredient
        self._current_id += 1

    def get_by_id(self, inventory_ingredient_id):
        inventory_ingredient_to_return = self._inventory_ingredients[
            inventory_ingredient_id
        ]
        inventory_ingredient_filtered = list(
            filter(
                lambda inventory_ingredient: inventory_ingredient.entity_status
                == Status.ACTIVE,
                [inventory_ingredient_to_return],
            )
        )
        return inventory_ingredient_filtered[0]

    def get_all(self):
        inventory_ingredients = list(self._inventory_ingredients.values())
        inventory_ingredients_filtered = filter(
            lambda inventory_ingredient: inventory_ingredient.entity_status
            == Status.ACTIVE,
            inventory_ingredients,
        )
        return list(inventory_ingredients_filtered)

    def delete_by_id(self, inventory_ingredient_id, inventory_ingredient):
        inventory_ingredient_to_be_delete = self.get_by_id(inventory_ingredient_id)
        inventory_ingredient_to_be_delete.entity_status = Status.DELETED
        inventory_ingredient_to_be_delete.updated_date = datetime.now()
        inventory_ingredient_to_be_delete.updated_by = inventory_ingredient.updated_by
        self._update_by_id(
            inventory_ingredient_id,
            inventory_ingredient_to_be_delete,
            use_merge_with_existing=False,
        )

    def update_by_id(self, inventory_ingredient_id, inventory_ingredient):
        self._update_by_id(inventory_ingredient_id, inventory_ingredient)

    def _update_by_id(
        self,
        inventory_ingredient_id,
        inventory_ingredient,
        use_merge_with_existing=True,
    ):
        current_inventory_ingredient = (
            self.get_by_id(inventory_ingredient_id)
            if use_merge_with_existing
            else inventory_ingredient
        )
        current_inventory_ingredient.inventory_id = (
            inventory_ingredient.inventory_id
            or current_inventory_ingredient.inventory_id
        )
        current_inventory_ingredient.ingredient_id = (
            inventory_ingredient.ingredient_id
            or current_inventory_ingredient.ingredient_id
        )
        current_inventory_ingredient.quantity = (
            inventory_ingredient.quantity
            or current_inventory_ingredient.quantity
        )
        current_inventory_ingredient.updated_date = datetime.now()
        current_inventory_ingredient.updated_by = (
            inventory_ingredient.updated_by or current_inventory_ingredient.updated_by
        )
        current_inventory_ingredient.entity_status = (
            inventory_ingredient.entity_status or current_inventory_ingredient
        )

    def get_by_ingredient_id(self, ingredient_id):
        inventory_ingredients = self.get_all()
        inventory_ingredient_by_ingredient_id = filter(
            (
                lambda inventory_ingredient: inventory_ingredient.ingredient_id
                == ingredient_id
            ),
            inventory_ingredients,
        )
        return list(inventory_ingredient_by_ingredient_id)

    def validate_ingredient_availability(
        self, inventory_id, ingredient_id, quantity_to_use
    ):

        inventory_ingredients = self.get_all()
        ingredient_to_validate = list(
            filter(
                (
                    lambda inventory_ingredient: inventory_ingredient.ingredient_id
                    == ingredient_id
                    and inventory_ingredient.inventory_id == inventory_id
                ),
                inventory_ingredients,
            )
        )
        if ingredient_to_validate[0].quantity > quantity_to_use:
            return True
        return False

    def get_final_product_qty_by_product_ids(self, product_ids):

        reduce_products_qty_array_to_final_products_qty_map = (
            setup_products_qty_array_to_final_products_qty_map(
                self.get_by_ingredient_id,
                self.product_ingredient_repository.get_by_product_id,
            )
        )

        final_product_possible_qty_map = (
            reduce_products_qty_array_to_final_products_qty_map(product_ids)
        )

        return final_product_possible_qty_map
