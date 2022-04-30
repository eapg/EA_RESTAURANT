import unittest
from unittest import mock

from src.api.controllers.inventory_controller import InventoryController
from src.lib.repositories.impl.inventory_repository_impl import \
    InventoryRepositoryImpl
from src.tests.utils.fixtures.inventory_fixture import (build_inventories,
                                                        build_inventory)


class InventoryIngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory_repository = mock.Mock(wraps=InventoryRepositoryImpl())
        self.inventory_controller = InventoryController(self.inventory_repository)

    def test_add_inventory_to_repository_using_controller(self):
        inventory = build_inventory()

        self.assertIsNone(inventory.id)

        self.inventory_controller.add(inventory)
        self.inventory_repository.add.assert_called_with(inventory)

    def test_get_inventory_from_repository_using_controller(self):
        inventories = build_inventories(count=3)

        self.inventory_controller.add(inventories[0])
        self.inventory_controller.add(inventories[1])
        self.inventory_controller.add(inventories[2])

        found_inventory3 = self.inventory_controller.get_by_id(3)

        self.inventory_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_inventory3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory(self):
        inventory1 = build_inventory()

        self.inventory_controller.add(inventory1)

        self.assertRaises(KeyError, self.inventory_controller.get_by_id, 2)
        self.inventory_repository.get_by_id.assert_called_with(2)

    def test_get_all_inventories_from_repository_using_controller(self):

        inventories_to_insert = build_inventories(count=4)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])
        self.inventory_controller.add(inventories_to_insert[2])
        self.inventory_controller.add(inventories_to_insert[3])

        inventories = self.inventory_controller.get_all()

        self.inventory_repository.get_all.assert_called_with()

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[2],
                inventories_to_insert[3],
            ],
        )

    def test_get_all_inventories_empty_from_repository_through_controller(
        self,
    ):
        inventories = self.inventory_controller.get_all()
        self.inventory_repository.get_all.assert_called_with()
        self.assertEqual(inventories, [])

    def test_delete_an_inventory_from_repository_using_controller(self):
        inventories_to_insert = build_inventories(count=4)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])
        self.inventory_controller.add(inventories_to_insert[2])
        self.inventory_controller.add(inventories_to_insert[3])

        self.inventory_controller.delete_by_id(3)
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_inventories(self):
        self.assertRaises(KeyError, self.inventory_controller.delete_by_id, 3)
        self.inventory_repository.delete_by_id.assert_called_with(3)

    def test_update_inventory_from_repository_using_controller(self):
        inventories_to_insert = build_inventories(count=2)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])

        inventory_list = [build_inventory()]

        inventory_to_update = build_inventory(inventory_ingredients=inventory_list)
        self.inventory_controller.update_by_id(2, inventory_to_update)
        updated_inventory = self.inventory_controller.get_by_id(2)
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.update_by_id.assert_called_once_with(
            2, inventory_to_update
        )

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.inventory_ingredients,
            inventory_to_update.inventory_ingredients,
        )
