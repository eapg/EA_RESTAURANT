import unittest
from unittest import mock

from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.constants.audit import Status
from src.lib.repositories.impl.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_fixture import build_inventory
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
    build_inventory_ingredients,
)


class InventoryIngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory_ingredient_repository = mock.Mock(
            wraps=InventoryIngredientRepositoryImpl()
        )
        self.inventory_ingredient_controller = InventoryIngredientController(
            self.inventory_ingredient_repository
        )

    def test_add_inventory_ingredient_to_repository_using_controller(self):
        inventory_ingredient = build_inventory_ingredient()

        self.assertIsNone(inventory_ingredient.id)

        self.inventory_ingredient_controller.add(inventory_ingredient)
        self.inventory_ingredient_repository.add.assert_called_with(
            inventory_ingredient
        )

    def test_get_inventory_ingredient_from_repository_using_controller(self):
        inventory_ingredients = build_inventory_ingredients(count=3)

        self.inventory_ingredient_controller.add(inventory_ingredients[0])
        self.inventory_ingredient_controller.add(inventory_ingredients[1])
        self.inventory_ingredient_controller.add(inventory_ingredients[2])

        found_inventory_ingredient3 = self.inventory_ingredient_controller.get_by_id(3)

        self.inventory_ingredient_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_inventory_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory_ingredient(self):
        inventory_ingredient1 = build_inventory_ingredient()

        self.inventory_ingredient_controller.add(inventory_ingredient1)

        self.assertRaises(KeyError, self.inventory_ingredient_controller.get_by_id, 2)
        self.inventory_ingredient_repository.get_by_id.assert_called_with(2)

    def test_get_all_inventory_ingredients_from_repository_using_controller(self):

        inventory_ingredients_to_insert = build_inventory_ingredients(count=4)

        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[0])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[1])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[2])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[3])

        inventory_ingredients = self.inventory_ingredient_controller.get_all()

        self.inventory_ingredient_repository.get_all.assert_called_with()

        self.assertEqual(
            inventory_ingredients,
            [
                inventory_ingredients_to_insert[0],
                inventory_ingredients_to_insert[1],
                inventory_ingredients_to_insert[2],
                inventory_ingredients_to_insert[3],
            ],
        )

    def test_get_all_inventory_ingredients_empty_from_repository_through_controller(
        self,
    ):
        inventory_ingredients = self.inventory_ingredient_controller.get_all()
        self.inventory_ingredient_repository.get_all.assert_called_with()
        self.assertEqual(inventory_ingredients, [])

    def test_delete_an_inventory_ingredient_from_repository_using_controller(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=4)
        inventory_ingredient_to_delete = build_inventory_ingredient(
            entity_status=Status.DELETED
        )
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[0])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[1])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[2])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[3])

        self.inventory_ingredient_controller.delete_by_id(
            3, inventory_ingredient_to_delete
        )
        inventory_ingredients = self.inventory_ingredient_controller.get_all()

        self.inventory_ingredient_repository.delete_by_id.assert_called_once_with(
            3, inventory_ingredient_to_delete
        )

        self.assertEqual(
            inventory_ingredients,
            [
                inventory_ingredients_to_insert[0],
                inventory_ingredients_to_insert[1],
                inventory_ingredients_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_inventory_ingredients(self):
        inventory_ingredient_to_delete = build_inventory_ingredient(
            entity_status=Status.DELETED
        )
        self.assertRaises(
            KeyError,
            self.inventory_ingredient_controller.delete_by_id,
            3,
            inventory_ingredient_to_delete,
        )
        self.inventory_ingredient_repository.delete_by_id.assert_called_with(
            3, inventory_ingredient_to_delete
        )

    def test_update_inventory_ingredient_from_repository_using_controller(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=2)

        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[0])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[1])

        inventory_ingredient_to_update = build_inventory_ingredient(
            ingredient_quantity=2
        )

        self.inventory_ingredient_controller.update_by_id(
            2, inventory_ingredient_to_update
        )
        updated_inventory_ingredient = self.inventory_ingredient_controller.get_by_id(2)
        inventory_ingredients = self.inventory_ingredient_controller.get_all()

        self.inventory_ingredient_repository.update_by_id.assert_called_once_with(
            2, inventory_ingredient_to_update
        )

        self.assertEqual(len(inventory_ingredients), 2)
        self.assertEqual(
            updated_inventory_ingredient.ingredient_quantity,
            inventory_ingredient_to_update.ingredient_quantity,
        )

    def test_get_by_ingredient_id_from_repository_using_controller(self):
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")
        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id, ingredient_quantity=10
        )
        inventory_ingredient_2 = build_inventory_ingredient()

        self.inventory_ingredient_controller.add(inventory_ingredient_1)
        self.inventory_ingredient_controller.add(inventory_ingredient_2)

        inventory_ingredient_returned = (
            self.inventory_ingredient_controller.get_by_ingredient_id(ingredient_1)
        )
        self.inventory_ingredient_repository.get_by_ingredient_id.assert_called_with(
            ingredient_1
        )

    def test_validate_ingredient_availability_from_repository_using_controller(self):

        inventory_1 = build_inventory(inventory_id=1)
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")

        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id,
            inventory_id=inventory_1.id,
            ingredient_quantity=10,
        )
        self.inventory_ingredient_controller.add(inventory_ingredient_1)
        self.inventory_ingredient_controller.validate_ingredient_availability(
            inventory_1.id, ingredient_1.id, 10
        )
        self.inventory_ingredient_repository.validate_ingredient_availability.assert_called_with(
            inventory_1.id, ingredient_1.id, 10
        )
