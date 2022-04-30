import unittest

from src.lib.repositories.impl.ingredient_repository_impl import (
    IngredientRepositoryImpl,
)
from src.tests.utils.fixtures.ingredient_fixture import (
    build_ingredient,
    build_ingredients,
)


class IngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_ingredient_successfully(self):
        ingredient = build_ingredient()
        ingredient_repository = IngredientRepositoryImpl()

        self.assertIsNone(ingredient.id)

        ingredient_repository.add(ingredient)

        self.assertEqual(ingredient.id, 1)

    def test_get_ingredient_successfully(self):
        ingredients = build_ingredients(count=3)

        ingredient_repository = IngredientRepositoryImpl()

        ingredient_repository.add(ingredients[0])
        ingredient_repository.add(ingredients[1])
        ingredient_repository.add(ingredients[2])

        found_ingredient3 = ingredient_repository.get_by_id(3)

        self.assertEqual(found_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_ingredient(self):
        ingredient1 = build_ingredient()

        ingredient_repository = IngredientRepositoryImpl()

        ingredient_repository.add(ingredient1)

        self.assertRaises(KeyError, ingredient_repository.get_by_id, 2)

    def test_get_all_ingredients_successfully(self):
        ingredients_to_insert = build_ingredients(count=5)

        ingredient_repository = IngredientRepositoryImpl()

        ingredient_repository.add(ingredients_to_insert[0])
        ingredient_repository.add(ingredients_to_insert[1])
        ingredient_repository.add(ingredients_to_insert[2])
        ingredient_repository.add(ingredients_to_insert[3])
        ingredient_repository.add(ingredients_to_insert[4])

        ingredients = ingredient_repository.get_all()

        self.assertEqual(
            ingredients,
            [
                ingredients_to_insert[0],
                ingredients_to_insert[1],
                ingredients_to_insert[2],
                ingredients_to_insert[3],
                ingredients_to_insert[4],
            ],
        )

    def test_get_all_ingredients_empty_successfully(self):
        ingredient_repository = IngredientRepositoryImpl()

        ingredients = ingredient_repository.get_all()

        self.assertEqual(ingredients, [])

    def test_delete_an_ingredient_successfully(self):
        ingredients_to_insert = build_ingredients(count=3)

        ingredient_repository = IngredientRepositoryImpl()

        ingredient_repository.add(ingredients_to_insert[0])
        ingredient_repository.add(ingredients_to_insert[1])
        ingredient_repository.add(ingredients_to_insert[2])

        ingredient_repository.delete_by_id(2)

        ingredients = ingredient_repository.get_all()

        self.assertEqual(
            ingredients, [ingredients_to_insert[0], ingredients_to_insert[2]]
        )

    def test_delete_throws_key_error_when_there_are_no_ingredients(self):
        ingredient_repository = IngredientRepositoryImpl()

        self.assertRaises(KeyError, ingredient_repository.delete_by_id, 2)

    def test_update_ingredient_successfully(self):
        ingredients_to_insert = build_ingredients(count=2)

        ingredient_repository = IngredientRepositoryImpl()

        ingredient_repository.add(ingredients_to_insert[0])
        ingredient_repository.add(ingredients_to_insert[1])

        ingredient_to_update = build_ingredient(name="updated-name")

        ingredient_repository.update_by_id(2, ingredient_to_update)
        updated_ingredient = ingredient_repository.get_by_id(2)
        ingredients = ingredient_repository.get_all()

        self.assertEqual(len(ingredients), 2)
        self.assertEqual(updated_ingredient.name, ingredient_to_update.name)
