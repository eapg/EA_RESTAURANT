import unittest

from src.lib.repositories.impl.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
    build_inventory_ingredients,
)
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient


class InventoryIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_inventory_ingredient_successfully(self):
        inventory_ingredient = build_inventory_ingredient()
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        self.assertIsNone(inventory_ingredient.id)

        inventory_ingredient_repository.add(inventory_ingredient)

        self.assertEqual(inventory_ingredient.id, 1)

    def test_get_inventory_ingredient_successfully(self):
        inventory_ingredients = build_inventory_ingredients(count=3)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients[0])
        inventory_ingredient_repository.add(inventory_ingredients[1])
        inventory_ingredient_repository.add(inventory_ingredients[2])

        found_inventory_ingredient3 = inventory_ingredient_repository.get_by_id(3)

        self.assertEqual(found_inventory_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory_ingredient(self):
        inventory_ingredient1 = build_inventory_ingredient()

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredient1)

        self.assertRaises(KeyError, inventory_ingredient_repository.get_by_id, 2)

    def test_get_all_inventory_ingredients_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=5)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[2])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[3])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[4])

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(
            inventory_ingredients,
            [
                inventory_ingredients_to_insert[0],
                inventory_ingredients_to_insert[1],
                inventory_ingredients_to_insert[2],
                inventory_ingredients_to_insert[3],
                inventory_ingredients_to_insert[4],
            ],
        )

    def test_get_all_inventory_ingredients_empty_successfully(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(inventory_ingredients, [])

    def test_delete_an_inventory_ingredient_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=3)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[2])

        inventory_ingredient_repository.delete_by_id(2)

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(
            inventory_ingredients,
            [inventory_ingredients_to_insert[0], inventory_ingredients_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_inventory_ingredients(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        self.assertRaises(KeyError, inventory_ingredient_repository.delete_by_id, 2)

    def test_update_inventory_ingredient_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=2)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])

        inventory_ingredient_to_update = build_inventory_ingredient(
            ingredient_quantity=2
        )

        inventory_ingredient_repository.update_by_id(2, inventory_ingredient_to_update)
        updated_inventory_ingredient = inventory_ingredient_repository.get_by_id(2)
        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(len(inventory_ingredients), 2)
        self.assertEqual(
            updated_inventory_ingredient.ingredient_quantity,
            inventory_ingredient_to_update.ingredient_quantity,
        )

    def test_get_by_ingredient_id_successfully(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")
        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient=ingredient_1, ingredient_quantity=10
        )
        inventory_ingredient_2 = build_inventory_ingredient()

        inventory_ingredient_repository.add(inventory_ingredient_1)
        inventory_ingredient_repository.add(inventory_ingredient_2)

        inventory_ingredient_returned = (
            inventory_ingredient_repository.get_by_ingredient_id(ingredient_1)
        )
        self.assertEqual(inventory_ingredient_returned[0], inventory_ingredient_1)
