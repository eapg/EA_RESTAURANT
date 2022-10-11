import unittest
from unittest import mock

from src.api.controllers.ingredient_controller import IngredientController

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_ingredient,
    build_ingredients,
)


class IngredientRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.ingredient_repository = mock.Mock()
        self.ingredient_controller = IngredientController(self.ingredient_repository)

    def test_add_ingredient_successfully(self):

        ingredient = build_ingredient()

        self.ingredient_controller.add(ingredient)

        self.ingredient_repository.add.assert_called_with(ingredient)

    def test_get_ingredient_successfully(self):

        ingredient = build_ingredient()

        self.ingredient_repository.get_by_id.return_value = ingredient

        expected_ingredient = self.ingredient_controller.get_by_id(ingredient.id)

        self.ingredient_repository.get_by_id.assert_called_with(ingredient.id)
        self.assertEqual(expected_ingredient.id, ingredient.id)

    def test_get_all_ingredients_successfully(self):

        ingredients = build_ingredients(count=3)

        self.ingredient_repository.get_all.return_value = ingredients

        expected_ingredients = self.ingredient_controller.get_all()

        self.ingredient_repository.get_all.assert_called()
        self.assertEqual(expected_ingredients, ingredients)
        self.assertEqual(len(expected_ingredients), 3)

    def test_delete_an_ingredient_successfully(self):

        ingredient_to_delete = build_ingredient()
        self.ingredient_controller.delete_by_id(2, ingredient_to_delete)

        self.ingredient_repository.delete_by_id.assert_called_with(
            2, ingredient_to_delete
        )

    def test_update_an_ingredient_successfully(self):

        ingredient = build_ingredient()

        self.ingredient_controller.update_by_id(1, ingredient)

        self.ingredient_repository.update_by_id.assert_called_with(1, ingredient)
