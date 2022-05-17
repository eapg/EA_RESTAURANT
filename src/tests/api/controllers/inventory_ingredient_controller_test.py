import unittest
from unittest import mock

from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_fixture import build_inventory
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
    build_inventory_ingredients,
)


class InventoryIngredientRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory_ingredient_repository = mock.Mock()
        self.inventory_ingredient_controller = InventoryIngredientController(
            self.inventory_ingredient_repository
        )

    def test_add_inventory_ingredient_successfully(self):
        inventory_ingredient = build_inventory_ingredient()

        self.inventory_ingredient_controller.add(inventory_ingredient)

        self.inventory_ingredient_repository.add.assert_called_with(
            inventory_ingredient
        )

    def test_get_inventory_ingredient_successfully(self):
        inventory_ingredient = build_inventory_ingredient()

        self.inventory_ingredient_repository.get_by_id.return_value = (
            inventory_ingredient
        )

        expected_inventory_ingredient = self.inventory_ingredient_controller.get_by_id(
            inventory_ingredient.id
        )

        self.inventory_ingredient_repository.get_by_id.assert_called_with(
            inventory_ingredient.id
        )
        self.assertEqual(expected_inventory_ingredient.id, inventory_ingredient.id)

    def test_get_all_inventory_ingredients_successfully(self):
        inventory_ingredients = build_inventory_ingredients(count=3)

        self.inventory_ingredient_repository.get_all.return_value = (
            inventory_ingredients
        )

        expected_inventory_ingredients = self.inventory_ingredient_controller.get_all()

        self.inventory_ingredient_repository.get_all.assert_called()
        self.assertEqual(expected_inventory_ingredients, inventory_ingredients)
        self.assertEqual(len(expected_inventory_ingredients), 3)

    def test_delete_an_inventory_ingredient_successfully(self):
        self.inventory_ingredient_controller.delete_by_id(2)

        self.inventory_ingredient_repository.delete_by_id.assert_called_with(2)

    def test_update_an_inventory_ingredient_successfully(self):
        inventory_ingredient = build_inventory_ingredient()

        self.inventory_ingredient_controller.update_by_id(1, inventory_ingredient)

        self.inventory_ingredient_repository.update_by_id.assert_called_with(
            1, inventory_ingredient
        )

    def test_get_by_ingredient_id(self):
        ingredient = build_ingredient()

        self.inventory_ingredient_controller.get_by_ingredient_id(ingredient)
        self.inventory_ingredient_repository.get_by_ingredient_id.assert_called_with(
            ingredient
        )

    def test_validate_ingredient_availability_successfully(self):
        ingredient = build_ingredient()
        inventory = build_inventory()
        quantity_to_use = 10
        self.inventory_ingredient_controller.validate_ingredient_availability(
            inventory.id, ingredient.id, quantity_to_use
        )
        self.inventory_ingredient_repository.validate_ingredient_availability.assert_called_with(
            inventory.id, ingredient.id, quantity_to_use
        )
