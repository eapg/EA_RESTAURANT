import unittest
from unittest import mock
from src.constants.audit import Status
from src.lib.repositories.impl.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.lib.repositories.impl.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
    build_inventory_ingredients,
)
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_fixture import build_inventory
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.product_fixture import build_product
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient


class InventoryIngredientRepositoryImplTestCase(unittest.TestCase):
    def test_add_inventory_ingredient_successfully(self):
        inventory_ingredient = build_inventory_ingredient()
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredient)

        self.assertEqual(inventory_ingredient.id, 1)

    def test_get_inventory_ingredient_successfully(self):
        inventory_ingredients = build_inventory_ingredients(count=3)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients[0])
        inventory_ingredient_repository.add(inventory_ingredients[1])
        inventory_ingredient_repository.add(inventory_ingredients[2])

        found_inventory_ingredient3 = inventory_ingredient_repository.get_by_id(3)

        self.assertEqual(found_inventory_ingredient3.id, 3)

    def test_get_throws_key_error_for_non_existing_inventory_ingredient(self):
        inventory_ingredient1 = build_inventory_ingredient()

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredient1)

        self.assertRaises(KeyError, inventory_ingredient_repository.get_by_id, 2)

    def test_get_all_inventory_ingredients_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=5)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[2])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[3])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[4])

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(
            inventory_ingredients,
            [
                inventory_ingredients_to_insert[0],
                inventory_ingredients_to_insert[1],
                inventory_ingredients_to_insert[2],
                inventory_ingredients_to_insert[3],
                inventory_ingredients_to_insert[4],
            ],
        )

    def test_get_all_inventory_ingredients_empty_successfully(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(inventory_ingredients, [])

    def test_delete_an_inventory_ingredient_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=3)
        inventory_ingredient_to_delete = build_inventory_ingredient(
            entity_status=Status.DELETED
        )
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[2])

        inventory_ingredient_repository.delete_by_id(2, inventory_ingredient_to_delete)

        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(
            inventory_ingredients,
            [inventory_ingredients_to_insert[0], inventory_ingredients_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_inventory_ingredients(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()
        inventory_ingredient_to_delete = build_inventory_ingredient(
            entity_status=Status.DELETED
        )
        self.assertRaises(
            KeyError,
            inventory_ingredient_repository.delete_by_id,
            2,
            inventory_ingredient_to_delete,
        )

    def test_update_inventory_ingredient_successfully(self):
        inventory_ingredients_to_insert = build_inventory_ingredients(count=2)

        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()

        inventory_ingredient_repository.add(inventory_ingredients_to_insert[0])
        inventory_ingredient_repository.add(inventory_ingredients_to_insert[1])

        inventory_ingredient_to_update = build_inventory_ingredient(
            ingredient_quantity=2
        )

        inventory_ingredient_repository.update_by_id(2, inventory_ingredient_to_update)
        updated_inventory_ingredient = inventory_ingredient_repository.get_by_id(2)
        inventory_ingredients = inventory_ingredient_repository.get_all()

        self.assertEqual(len(inventory_ingredients), 2)
        self.assertEqual(
            updated_inventory_ingredient.ingredient_quantity,
            inventory_ingredient_to_update.ingredient_quantity,
        )

    def test_get_by_ingredient_id_successfully(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")
        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id, ingredient_quantity=10
        )
        inventory_ingredient_2 = build_inventory_ingredient()

        inventory_ingredient_repository.add(inventory_ingredient_1)
        inventory_ingredient_repository.add(inventory_ingredient_2)

        inventory_ingredient_returned = (
            inventory_ingredient_repository.get_by_ingredient_id(ingredient_1.id)
        )
        self.assertEqual(inventory_ingredient_returned[0], inventory_ingredient_1)

    def test_validate_ingredient_availability(self):
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl()
        inventory_1 = build_inventory(inventory_id=1)
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient test")

        inventory_ingredient_1 = build_inventory_ingredient(
            ingredient_id=ingredient_1.id,
            inventory_id=inventory_1.id,
            ingredient_quantity=10,
        )
        inventory_ingredient_repository.add(inventory_ingredient_1)
        self.assertTrue(
            inventory_ingredient_repository.validate_ingredient_availability(
                inventory_1.id, ingredient_1.id, 5
            )
        )
        self.assertFalse(
            inventory_ingredient_repository.validate_ingredient_availability(
                inventory_1.id, ingredient_1.id, 15
            )
        )

    def test_get_quantity_of_product_that_can_be_made_by_product_ids(self):

        product_ingredient_repository = mock.Mock(
            wraps=ProductIngredientRepositoryImpl()
        )
        ingredient_1 = build_ingredient(ingredient_id=1, name="test_ingredient")
        inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1,
            ingredient_id=ingredient_1.id,
            ingredient_quantity=20,
        )
        product_1 = build_product(product_id=1)
        product_ingredient_1 = build_product_ingredient(
            id=1, ingredient_id=ingredient_1.id, product_id=product_1.id, quantity=2
        )
        order_detail_1 = build_order_detail(
            order_detail_id=1, product_id=product_1.id, quantity=1
        )
        product_ingredient_repository.add(product_ingredient_1)
        inventory_ingredient_repository = InventoryIngredientRepositoryImpl(
            product_ingredient_repository
        )
        inventory_ingredient_repository.get_by_ingredient_id = mock.Mock(
            wraps=inventory_ingredient_repository.get_by_ingredient_id
        )
        inventory_ingredient_repository.add(inventory_ingredient_1)
        product_quantity = (
            inventory_ingredient_repository.get_final_product_qty_by_product_ids(
                [order_detail_1.product_id]
            )
        )

        self.assertEqual(product_quantity[order_detail_1.product_id], 10)
        product_ingredient_repository.get_by_product_id.assert_called_with(product_1.id)
        inventory_ingredient_repository.get_by_ingredient_id.assert_called_with(
            product_ingredient_1.ingredient_id
        )
