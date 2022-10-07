import unittest
from unittest import mock

from src.api.controllers.inventory_ingredient_controller import (
    InventoryIngredientController,
)
from src.constants.audit import Status
from src.lib.repositories.impl_v2.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_inventory_ingredient,
    build_inventory_ingredients,
    build_inventory,
    build_ingredient,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class InventoryIngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.inventory_ingredient_repository = mock.Mock(
            wraps=InventoryIngredientRepositoryImpl(self.mocked_sqlalchemy_session)
        )
        self.inventory_ingredient_controller = InventoryIngredientController(
            self.inventory_ingredient_repository
        )

    def test_add_inventory_ingredient_to_repository_using_controller(self):
        inventory_ingredient = build_inventory_ingredient()

        self.inventory_ingredient_controller.add(inventory_ingredient)
        self.inventory_ingredient_repository.add.assert_called_with(
            inventory_ingredient
        )

    def test_get_inventory_ingredient_from_repository_using_controller(self):
        inventory_ingredients = build_inventory_ingredients(count=3)

        self.inventory_ingredient_controller.add(inventory_ingredients[0])
        self.inventory_ingredient_controller.add(inventory_ingredients[1])
        self.inventory_ingredient_controller.add(inventory_ingredients[2])
        self.inventory_ingredient_repository.get_by_id.return_value = (
            inventory_ingredients[2]
        )
        found_inventory_ingredient2 = self.inventory_ingredient_controller.get_by_id(2)

        self.inventory_ingredient_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_inventory_ingredient2.id, 2)

    def test_get_all_inventory_ingredients_from_repository_using_controller(self):

        inventory_ingredients_to_insert = build_inventory_ingredients(count=4)

        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[0])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[1])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[2])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[3])
        self.inventory_ingredient_repository.get_all.return_value = (
            inventory_ingredients_to_insert
        )
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
        self.inventory_ingredient_repository.get_all.return_value = []
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
        self.inventory_ingredient_repository.get_all.return_value = [
            inventory_ingredients_to_insert[0],
            inventory_ingredients_to_insert[1],
            inventory_ingredients_to_insert[3],
        ]
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

    def test_update_inventory_ingredient_from_repository_using_controller(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=2)

        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[0])
        self.inventory_ingredient_controller.add(inventory_ingredients_to_insert[1])

        inventory_ingredient_to_update = build_inventory_ingredient(quantity=2)

        self.inventory_ingredient_controller.update_by_id(
            2, inventory_ingredient_to_update
        )
        self.inventory_ingredient_repository.get_by_id.return_value = (
            inventory_ingredient_to_update
        )
        updated_inventory_ingredient = self.inventory_ingredient_controller.get_by_id(2)
        self.inventory_ingredient_repository.get_all.return_value = (
            inventory_ingredients_to_insert
        )
        inventory_ingredients = self.inventory_ingredient_controller.get_all()

        self.inventory_ingredient_repository.update_by_id.assert_called_once_with(
            2, inventory_ingredient_to_update
        )

        self.assertEqual(len(inventory_ingredients), 2)
        self.assertEqual(
            updated_inventory_ingredient.quantity,
            inventory_ingredient_to_update.quantity,
        )

    def test_get_by_ingredient_id_from_repository_using_controller(self):
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")
        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id, quantity=10
        )
        inventory_ingredient_2 = build_inventory_ingredient()

        self.inventory_ingredient_controller.add(inventory_ingredient_1)
        self.inventory_ingredient_controller.add(inventory_ingredient_2)
        self.inventory_ingredient_repository.get_by_ingredient_id.return_value = (
            inventory_ingredient_1
        )
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
            quantity=10,
        )
        self.inventory_ingredient_controller.add(inventory_ingredient_1)
        self.inventory_ingredient_controller.validate_ingredient_availability(
            inventory_1.id, ingredient_1.id, 10
        )
        self.inventory_ingredient_repository.validate_ingredient_availability.assert_called_with(
            inventory_1.id, ingredient_1.id, 10
        )
