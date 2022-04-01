import unittest
from unittest import mock

from src.api.controllers.ingredient_controller import IngredientController
from src.lib.repositories.impl.ingredient_repository_impl import (
    IngredientRepositoryImpl,
)
from src.tests.utils.fixtures.ingredient_fixture import (
    build_ingredient,
    build_ingredients,
)


class IngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.ingredient_repository = mock.Mock(wraps=IngredientRepositoryImpl())
        self.ingredient_controller = IngredientController(self.ingredient_repository)

    def test_add_ingredient_to_repository_using_controller(self):
        ingredient = build_ingredient()

        self.assertIsNone(ingredient.id)

        self.ingredient_controller.add(ingredient)
        self.ingredient_repository.add.assert_called_with(ingredient)

    def test_get_ingredient_from_repository_using_controller(self):
        ingredients = build_ingredients(count=3)

        self.ingredient_controller.add(ingredients[0])
        self.ingredient_controller.add(ingredients[1])
        self.ingredient_controller.add(ingredients[2])

        found_ingredient3 = self.ingredient_controller.get_by_id(3)

        self.ingredient_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_ingredient(self):
        ingredient1 = build_ingredient()

        self.ingredient_controller.add(ingredient1)

        self.assertRaises(KeyError, self.ingredient_controller.get_by_id, 2)
        self.ingredient_repository.get_by_id.assert_called_with(2)

    def test_get_all_ingredients_from_repository_using_controller(self):

        ingredients_to_insert = build_ingredients(count=4)

        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])
        self.ingredient_controller.add(ingredients_to_insert[2])
        self.ingredient_controller.add(ingredients_to_insert[3])

        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.get_all.assert_called_with()

        self.assertEqual(
            ingredients,
            [
                ingredients_to_insert[0],
                ingredients_to_insert[1],
                ingredients_to_insert[2],
                ingredients_to_insert[3],
            ],
        )

    def test_get_all_ingredients_empty_from_repository_through_controller(self):
        ingredients = self.ingredient_controller.get_all()
        self.ingredient_repository.get_all.assert_called_with()
        self.assertEqual(ingredients, [])

    def test_delete_an_ingredient_from_repository_using_controller(self):
        ingredients_to_insert = build_ingredients(count=4)

        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])
        self.ingredient_controller.add(ingredients_to_insert[2])
        self.ingredient_controller.add(ingredients_to_insert[3])

        self.ingredient_controller.delete_by_id(3)
        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            ingredients,
            [
                ingredients_to_insert[0],
                ingredients_to_insert[1],
                ingredients_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_ingredients(self):
        self.assertRaises(KeyError, self.ingredient_controller.delete_by_id, 3)
        self.ingredient_repository.delete_by_id.assert_called_with(3)

    def test_update_ingredient_from_repository_using_controller(self):
        ingredients_to_insert = build_ingredients(count=2)

        self.ingredient_controller.add(ingredients_to_insert[0])
        self.ingredient_controller.add(ingredients_to_insert[1])

        ingredient_to_update = build_ingredient(description="updated-description")

        self.ingredient_controller.update_by_id(2, ingredient_to_update)
        updated_ingredient = self.ingredient_controller.get_by_id(2)
        ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.update_by_id.assert_called_once_with(
            2, ingredient_to_update
        )

        self.assertEqual(len(ingredients), 2)
        self.assertEqual(
            updated_ingredient.description, ingredient_to_update.description
        )
