import unittest
from unittest import mock

from src.api.controllers import product_ingredient_controller
from src.constants import audit
from src.lib.repositories.impl import product_ingredient_repository_impl
from src.tests.utils.fixtures import ingredient_fixture
from src.tests.utils.fixtures import product_fixture
from src.tests.utils.fixtures import product_ingredient_fixture


class ProductIngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.product_ingredient_repository = mock.Mock(
            wraps=product_ingredient_repository_impl.ProductIngredientRepositoryImpl()
        )
        self.product_ingredient_controller = (
            product_ingredient_controller.ProductIngredientController(
                self.product_ingredient_repository
            )
        )

    def test_add_product_ingredient_to_repository_using_controller(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient)
        self.product_ingredient_repository.add.assert_called_with(product_ingredient)
        self.assertEqual(product_ingredient.id, 1)

    def test_get_product_ingredient_from_repository_using_controller(self):
        product_ingredients = product_ingredient_fixture.build_product_ingredients(
            count=3
        )

        self.product_ingredient_controller.add(product_ingredients[0])
        self.product_ingredient_controller.add(product_ingredients[1])
        self.product_ingredient_controller.add(product_ingredients[2])

        found_product_ingredient3 = self.product_ingredient_controller.get_by_id(3)

        self.product_ingredient_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_product_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_product_ingredient(self):
        product_ingredient1 = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient1)

        self.assertRaises(KeyError, self.product_ingredient_controller.get_by_id, 2)
        self.product_ingredient_repository.get_by_id.assert_called_with(2)

    def test_get_all_product_ingredients_from_repository_using_controller(self):

        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=4)
        )

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
        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=4)
        )
        product_ingredient_to_delete = (
            product_ingredient_fixture.build_product_ingredient(
                entity_status=audit.Status.DELETED
            )
        )
        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])
        self.product_ingredient_controller.add(product_ingredients_to_insert[2])
        self.product_ingredient_controller.add(product_ingredients_to_insert[3])

        self.product_ingredient_controller.delete_by_id(3, product_ingredient_to_delete)
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.delete_by_id.assert_called_once_with(
            3, product_ingredient_to_delete
        )

        self.assertEqual(
            product_ingredients,
            [
                product_ingredients_to_insert[0],
                product_ingredients_to_insert[1],
                product_ingredients_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_product_ingredients(self):
        product_ingredient_to_delete = (
            product_ingredient_fixture.build_product_ingredient(
                entity_status=audit.Status.DELETED
            )
        )
        self.assertRaises(
            KeyError,
            self.product_ingredient_controller.delete_by_id,
            3,
            product_ingredient_to_delete,
        )
        self.product_ingredient_repository.delete_by_id.assert_called_with(
            3, product_ingredient_to_delete
        )

    def test_update_product_ingredient_from_repository_using_controller(self):
        product_ingredients_to_insert = (
            product_ingredient_fixture.build_product_ingredients(count=2)
        )

        self.product_ingredient_controller.add(product_ingredients_to_insert[0])
        self.product_ingredient_controller.add(product_ingredients_to_insert[1])

        product_ingredient_to_update = (
            product_ingredient_fixture.build_product_ingredient(quantity=5)
        )

        self.product_ingredient_controller.update_by_id(2, product_ingredient_to_update)
        updated_product_ingredient = self.product_ingredient_controller.get_by_id(2)
        product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.update_by_id.assert_called_once_with(
            2, product_ingredient_to_update
        )

        self.assertEqual(len(product_ingredients), 2)
        self.assertEqual(
            updated_product_ingredient.quantity, product_ingredient_to_update.quantity
        )

    def test_get_by_product_id_from_repository_using_controller(self):
        ingredient_1 = ingredient_fixture.build_ingredient(
            ingredient_id=1, name="test ingredient"
        )
        product_1 = product_fixture.build_product(product_id=1, name="test product")
        product_ingredient_1 = product_ingredient_fixture.build_product_ingredient(
            ingredient_id=ingredient_1.id, product_id=product_1.id
        )
        product_ingredient_2 = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient_1)
        self.product_ingredient_controller.add(product_ingredient_2)

        product_ingredients_returned = (
            self.product_ingredient_controller.get_by_product_id(product_1.id)
        )
        self.product_ingredient_repository.get_by_product_id.assert_called_with(
            product_1.id
        )
