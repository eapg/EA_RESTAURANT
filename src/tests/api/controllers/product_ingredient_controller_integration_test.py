import unittest
from unittest import mock

from src.api.controllers.product_ingredient_controller import ProductIngredientController
from src.lib.repositories.impl.product_ingredient_repository_impl import ProductIngredientRepositoryImpl
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient, build_product_ingredients


class ProductIngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.product_ingredient_repository = mock.Mock(wraps=ProductIngredientRepositoryImpl())
        self.product_ingredient_controller = ProductIngredientController(self.product_ingredient_repository)

    def test_add_product_ingredient_to_repository_using_controller(self):
        product_ingredient = build_product_ingredient()

        self.assertIsNone(product_ingredient.id)

        self.product_ingredient_controller.add(product_ingredient)
        self.product_ingredient_repository.add.assert_called_with(product_ingredient)

    def test_get_product_ingredient_from_repository_using_controller(self):
        product_ingredients = build_product_ingredients(count=3)

        self.product_ingredient_controller.add(product_ingredients[0])
        self.product_ingredient_controller.add(product_ingredients[1])
        self.product_ingredient_controller.add(product_ingredients[2])

        found_product_ingredient3 = self.product_ingredient_controller.get_by_id(3)

        self.product_ingredient_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_product_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_product_ingredient(self):
        product_ingredient1 = build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient1)

        self.assertRaises(KeyError, self.product_ingredient_controller.get_by_id, 2)
        self.product_ingredient_repository.get_by_id.assert_called_with(2)

    def test_get_all_product_ingredients_from_repository_using_controller(self):

        product_ingredients_to_insert = build_product_ingredients(count=4)

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])
        self.product_ingredient_controller.add(product_ingredients_to_insert[2])
        self.product_ingredient_controller.add(product_ingredients_to_insert[3])

        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.get_all.assert_called_with()

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[2],
                product_ingredients_to_insert[3],
            ],
        )

    def test_get_all_product_ingredients_empty_from_repository_through_controller(self):
        product_ingredients = self.product_ingredient_controller.get_all()
        self.product_ingredient_repository.get_all.assert_called_with()
        self.assertEqual(product_ingredients, [])

    def test_delete_an_product_ingredient_from_repository_using_controller(self):
        product_ingredients_to_insert = build_product_ingredients(count=4)

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])
        self.product_ingredient_controller.add(product_ingredients_to_insert[2])
        self.product_ingredient_controller.add(product_ingredients_to_insert[3])

        self.product_ingredient_controller.delete_by_id(3)
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_product_ingredients(self):
        self.assertRaises(KeyError, self.product_ingredient_controller.delete_by_id, 3)
        self.product_ingredient_repository.delete_by_id.assert_called_with(3)

    def test_update_product_ingredient_from_repository_using_controller(self):
        product_ingredients_to_insert = build_product_ingredients(count=2)

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])

        product_ingredient_to_update = build_product_ingredient(quantity=5)

        self.product_ingredient_controller.update_by_id(2, product_ingredient_to_update)
        updated_product_ingredient = self.product_ingredient_controller.get_by_id(2)
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.update_by_id.assert_called_once_with(
            2, product_ingredient_to_update
        )

        self.assertEqual(len(product_ingredients), 2)
        self.assertEqual(updated_product_ingredient.quantity, product_ingredient_to_update.quantity)
