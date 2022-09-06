import unittest
from unittest import mock

from src.api.controllers import product_ingredient_controller
from src.constants import audit
from src.tests.utils.fixtures import product_fixture
from src.tests.utils.fixtures import product_ingredient_fixture


class ProductIngredientRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.product_ingredient_repository = mock.Mock()
        self.product_ingredient_controller = (
            product_ingredient_controller.ProductIngredientController(
                self.product_ingredient_repository
            )
        )

    def test_add_product_ingredient_successfully(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_controller.add(product_ingredient)

        self.product_ingredient_repository.add.assert_called_with(product_ingredient)

    def test_get_product_ingredient_successfully(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_repository.get_by_id.return_value = product_ingredient

        expected_product_ingredient = self.product_ingredient_controller.get_by_id(
            product_ingredient.id
        )

        self.product_ingredient_repository.get_by_id.assert_called_with(
            product_ingredient.id
        )
        self.assertEqual(expected_product_ingredient.id, product_ingredient.id)

    def test_get_all_product_ingredients_successfully(self):
        product_ingredients = product_ingredient_fixture.build_product_ingredients(
            count=3
        )

        self.product_ingredient_repository.get_all.return_value = product_ingredients

        expected_product_ingredients = self.product_ingredient_controller.get_all()

        self.product_ingredient_repository.get_all.assert_called()
        self.assertEqual(expected_product_ingredients, product_ingredients)
        self.assertEqual(len(expected_product_ingredients), 3)

    def test_delete_an_product_ingredient_successfully(self):
        product_ingredient_to_delete = (
            product_ingredient_fixture.build_product_ingredient(
                entity_status=audit.Status.DELETED
            )
        )
        self.product_ingredient_controller.delete_by_id(2, product_ingredient_to_delete)

        self.product_ingredient_repository.delete_by_id.assert_called_with(
            2, product_ingredient_to_delete
        )

    def test_update_an_product_ingredient_successfully(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()

        self.product_ingredient_controller.update_by_id(1, product_ingredient)

        self.product_ingredient_repository.update_by_id.assert_called_with(
            1, product_ingredient
        )

    def test_get_by_product_id_successfully(self):
        product_ingredient = product_ingredient_fixture.build_product_ingredient()
        product_1 = product_fixture.build_product()

        self.product_ingredient_repository.get_by_product_id.return_value = (
            product_ingredient
        )
        expected_product_ingredient = (
            self.product_ingredient_controller.get_by_product_id(product_1)
        )
        self.product_ingredient_repository.get_by_product_id.assert_called_with(
            product_1
        )
        self.assertEqual(expected_product_ingredient, product_ingredient)
