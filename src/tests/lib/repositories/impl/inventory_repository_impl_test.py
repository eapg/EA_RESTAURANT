import unittest

from src.constants import audit
from src.lib.repositories.impl import inventory_repository_impl
from src.tests.utils.fixtures import inventory_fixture


class InventoryIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_inventory_successfully(self):
        inventory = inventory_fixture.build_inventory()
        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventory)

        self.assertEqual(inventory.id, 1)

    def test_get_inventory_successfully(self):
        inventories = inventory_fixture.build_inventories(count=3)

        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventories[0])
        inventory_repository.add(inventories[1])
        inventory_repository.add(inventories[2])

        found_inventory3 = inventory_repository.get_by_id(3)

        self.assertEqual(found_inventory3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory(self):
        inventory1 = inventory_fixture.build_inventory()

        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventory1)

        self.assertRaises(KeyError, inventory_repository.get_by_id, 2)

    def test_get_all_inventories_successfully(self):
        inventories_to_insert = inventory_fixture.build_inventories(count=5)

        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])
        inventory_repository.add(inventories_to_insert[2])
        inventory_repository.add(inventories_to_insert[3])
        inventory_repository.add(inventories_to_insert[4])

        inventories = inventory_repository.get_all()

        self.assertEqual(
            inventories,
            [
                inventories_to_insert[0],
                inventories_to_insert[1],
                inventories_to_insert[2],
                inventories_to_insert[3],
                inventories_to_insert[4],
            ],
        )

    def test_get_all_inventories_empty_successfully(self):
        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventories = inventory_repository.get_all()

        self.assertEqual(inventories, [])

    def test_delete_an_inventory_successfully(self):
        inventories_to_insert = inventory_fixture.build_inventories(count=3)
        inventory_to_delete = inventory_fixture.build_inventory(
            entity_status=audit.Status.DELETED
        )
        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])
        inventory_repository.add(inventories_to_insert[2])

        inventory_repository.delete_by_id(2, inventory_to_delete)

        inventories = inventory_repository.get_all()

        self.assertEqual(
            inventories,
            [inventories_to_insert[0], inventories_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_inventories(self):
        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()
        inventory_to_delete = inventory_fixture.build_inventory(
            entity_status=audit.Status.DELETED
        )
        self.assertRaises(
            KeyError, inventory_repository.delete_by_id, 2, inventory_to_delete
        )

    def test_update_inventory_successfully(self):
        inventories_to_insert = inventory_fixture.build_inventories(count=2)

        inventory_repository = inventory_repository_impl.InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])

        inventory_to_update = inventory_fixture.build_inventory(update_by="test")

        inventory_repository.update_by_id(2, inventory_to_update)
        updated_inventory = inventory_repository.get_by_id(2)
        inventories = inventory_repository.get_all()

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.updated_by,
            inventory_to_update.updated_by,
        )
