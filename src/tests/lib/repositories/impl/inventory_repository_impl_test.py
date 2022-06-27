import unittest
from src.constants.audit import Status
from src.lib.repositories.impl.inventory_repository_impl import InventoryRepositoryImpl
from src.tests.utils.fixtures.inventory_fixture import (
    build_inventories,
    build_inventory,
)
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
)


class InventoryIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_inventory_successfully(self):
        inventory = build_inventory()
        inventory_repository = InventoryRepositoryImpl()

        self.assertIsNone(inventory.id)

        inventory_repository.add(inventory)

        self.assertEqual(inventory.id, 1)

    def test_get_inventory_successfully(self):
        inventories = build_inventories(count=3)

        inventory_repository = InventoryRepositoryImpl()

        inventory_repository.add(inventories[0])
        inventory_repository.add(inventories[1])
        inventory_repository.add(inventories[2])

        found_inventory3 = inventory_repository.get_by_id(3)

        self.assertEqual(found_inventory3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory(self):
        inventory1 = build_inventory()

        inventory_repository = InventoryRepositoryImpl()

        inventory_repository.add(inventory1)

        self.assertRaises(KeyError, inventory_repository.get_by_id, 2)

    def test_get_all_inventories_successfully(self):
        inventories_to_insert = build_inventories(count=5)

        inventory_repository = InventoryRepositoryImpl()

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
        inventory_repository = InventoryRepositoryImpl()

        inventories = inventory_repository.get_all()

        self.assertEqual(inventories, [])

    def test_delete_an_inventory_successfully(self):
        inventories_to_insert = build_inventories(count=3)
        inventory_to_delete = build_inventory(entity_status=Status.DELETED)
        inventory_repository = InventoryRepositoryImpl()

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
        inventory_repository = InventoryRepositoryImpl()
        inventory_to_delete = build_inventory(entity_status=Status.DELETED)
        self.assertRaises(
            KeyError, inventory_repository.delete_by_id, 2, inventory_to_delete
        )

    def test_update_inventory_successfully(self):
        inventories_to_insert = build_inventories(count=2)

        inventory_repository = InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])

        inventory_to_update = build_inventory(update_by="test")

        inventory_repository.update_by_id(2, inventory_to_update)
        updated_inventory = inventory_repository.get_by_id(2)
        inventories = inventory_repository.get_all()

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.update_by,
            inventory_to_update.update_by,
        )
