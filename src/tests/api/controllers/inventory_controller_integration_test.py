import unittest
from unittest import mock

from src.api.controllers import inventory_controller
from src.constants import audit
from src.lib.repositories.impl import inventory_repository_impl
from src.tests.utils.fixtures import inventory_fixture


class InventoryIngredientRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory_repository = mock.Mock(
            wraps=inventory_repository_impl.InventoryRepositoryImpl()
        )
        self.inventory_controller = inventory_controller.InventoryController(
            self.inventory_repository
        )

    def test_add_inventory_to_repository_using_controller(self):
        inventory = inventory_fixture.build_inventory()

        self.inventory_controller.add(inventory)
        self.inventory_repository.add.assert_called_with(inventory)
        self.assertEqual(inventory.id, 1)

    def test_get_inventory_from_repository_using_controller(self):
        inventories = inventory_fixture.build_inventories(count=3)

        self.inventory_controller.add(inventories[0])
        self.inventory_controller.add(inventories[1])
        self.inventory_controller.add(inventories[2])

        found_inventory3 = self.inventory_controller.get_by_id(3)

        self.inventory_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_inventory3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory(self):
        inventory1 = inventory_fixture.build_inventory()

        self.inventory_controller.add(inventory1)

        self.assertRaises(KeyError, self.inventory_controller.get_by_id, 2)
        self.inventory_repository.get_by_id.assert_called_with(2)

    def test_get_all_inventories_from_repository_using_controller(self):

        inventories_to_insert = inventory_fixture.build_inventories(count=4)

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
        inventories_to_insert = inventory_fixture.build_inventories(count=4)
        inventory_to_delete = inventory_fixture.build_inventory(
            entity_status=audit.Status.DELETED
        )
        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])
        self.inventory_controller.add(inventories_to_insert[2])
        self.inventory_controller.add(inventories_to_insert[3])

        self.inventory_controller.delete_by_id(3, inventory_to_delete)
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.delete_by_id.assert_called_once_with(
            3, inventory_to_delete
        )

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_inventories(self):
        inventory_to_delete = inventory_fixture.build_inventory(
            entity_status=audit.Status.DELETED
        )
        self.assertRaises(
            KeyError, self.inventory_controller.delete_by_id, 3, inventory_to_delete
        )
        self.inventory_repository.delete_by_id.assert_called_with(
            3, inventory_to_delete
        )

    def test_update_inventory_from_repository_using_controller(self):
        inventories_to_insert = inventory_fixture.build_inventories(count=2)

        self.inventory_controller.add(inventories_to_insert[0])
        self.inventory_controller.add(inventories_to_insert[1])

        inventory_list = [inventory_fixture.build_inventory()]

        inventory_to_update = inventory_fixture.build_inventory(update_by="test")
        self.inventory_controller.update_by_id(2, inventory_to_update)
        updated_inventory = self.inventory_controller.get_by_id(2)
        inventories = self.inventory_controller.get_all()

        self.inventory_repository.update_by_id.assert_called_once_with(
            2, inventory_to_update
        )

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.updated_by,
            inventory_to_update.updated_by,
        )
