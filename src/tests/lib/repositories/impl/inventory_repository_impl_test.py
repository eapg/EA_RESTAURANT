import unittest

from src.lib.repositories.impl.inventory_repository_impl import InventoryRepositoryImpl
from src.lib.repositories.impl.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.lib.repositories.impl.ingredient_repository_impl import (
    IngredientRepositoryImpl,
)

from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
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

        inventory_repository = InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])
        inventory_repository.add(inventories_to_insert[2])

        inventory_repository.delete_by_id(2)

        inventories = inventory_repository.get_all()

        self.assertEqual(
            inventories,
            [inventories_to_insert[0], inventories_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_inventories(self):
        inventory_repository = InventoryRepositoryImpl()

        self.assertRaises(KeyError, inventory_repository.delete_by_id, 2)

    def test_update_inventory_successfully(self):
        inventories_to_insert = build_inventories(count=2)

        inventory_repository = InventoryRepositoryImpl()

        inventory_repository.add(inventories_to_insert[0])
        inventory_repository.add(inventories_to_insert[1])

        inventory_ingredient_list = [build_inventory_ingredient()]

        inventory_to_update = build_inventory(
            inventory_ingredients=inventory_ingredient_list
        )

        inventory_repository.update_by_id(2, inventory_to_update)
        updated_inventory = inventory_repository.get_by_id(2)
        inventories = inventory_repository.get_all()

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_inventory.inventory_ingredients,
            inventory_to_update.inventory_ingredients,
        )

    def test_ingredient_availability(self):

        # repositories
        ingredient_repository = IngredientRepositoryImpl()
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()
        inventory_repository = InventoryRepositoryImpl(inventory_ingredient_repository)

        ingredient = build_ingredient(name="pizza")
        ingredient_repository.add(ingredient)
        ingredient_from_repository = ingredient_repository.get_by_id(1)

        inventory_ingredient = build_inventory_ingredient(
            ingredient=ingredient_from_repository, ingredient_quantity=50
        )
        inventory_ingredient_repository.add(inventory_ingredient)

        inventory = build_inventory()
        inventory.inventory_ingredients[
            ingredient.id
        ] = inventory_ingredient_repository.get_by_id(1)
        inventory_repository.add(inventory)

        self.assertTrue(
            inventory_repository.inventory_ingredient_availability(1, 1, 45)
        )
        self.assertFalse(
            inventory_repository.inventory_ingredient_availability(1, 1, 60)
        )
