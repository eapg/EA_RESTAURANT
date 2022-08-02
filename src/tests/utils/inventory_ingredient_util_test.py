import unittest
from unittest.mock import Mock, patch

from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
)
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient
from src.utils.inventory_ingredient_util import (
    products_qty_by_ingredients_qty_reducer,
    products_qty_array_to_final_products_qty_map_reducer,
    setup_products_qty_array_to_final_products_qty_map,
)


def get_inventory_ingredient_by_ingredient_id_mock(ingredient_id):

    inventory_ingredient_1 = build_inventory_ingredient(
        inventory_ingredient_id=1, ingredient_id=1, ingredient_quantity=20
    )
    inventory_ingredient_2 = build_inventory_ingredient(
        inventory_ingredient_id=2, ingredient_id=2, ingredient_quantity=30
    )
    inventory_ingredients = {1: inventory_ingredient_1, 2: inventory_ingredient_2}
    return [inventory_ingredients[ingredient_id]]


def get_product_ingredient_by_product_id_mock(product_id):
    product_ingredient_1 = build_product_ingredient(
        product_ingredient_id=1, product_id=1, ingredient_id=1, quantity=2
    )
    product_ingredient_2 = build_product_ingredient(
        product_ingredient_id=2, product_id=2, ingredient_id=2, quantity=4
    )
    product_ingredients = {1: product_ingredient_1, 2: product_ingredient_2}
    return [product_ingredients[product_id]]


class TestInventoryIngredient(unittest.TestCase):
    def test_quantity_ingredients_by_product_reducer(self):
        ingredient = build_ingredient(ingredient_id=1, name="ingredient test")
        product_ingredient = build_product_ingredient(
            product_ingredient_id=1, ingredient_id=ingredient.id, quantity=2
        )
        inventory_ingredient = build_inventory_ingredient(
            inventory_ingredient_id=1, ingredient_id=1, ingredient_quantity=20
        )

        quantity_ingredients_to_prepare_product = (
            products_qty_by_ingredients_qty_reducer(
                [], product_ingredient, [inventory_ingredient]
            )
        )
        self.assertEqual(quantity_ingredients_to_prepare_product[0], 10)

    def test_products_qty_array_to_final_products_qty_map_reducer(self):
        ingredient = build_ingredient(ingredient_id=1, name="ingredient test")
        product_ingredient = build_product_ingredient(
            product_ingredient_id=1, ingredient_id=ingredient.id, quantity=2
        )
        inventory_ingredient = build_inventory_ingredient(
            inventory_ingredient_id=1, ingredient_id=1, ingredient_quantity=20
        )

        quantity_ingredients_to_prepare_product = (
            products_qty_by_ingredients_qty_reducer(
                [], product_ingredient, [inventory_ingredient]
            )
        )

        final_product_qty_result_map = (
            products_qty_array_to_final_products_qty_map_reducer(
                {},
                product_ingredient.product_id,
                quantity_ingredients_to_prepare_product,
            )
        )
        self.assertEqual(
            final_product_qty_result_map[product_ingredient.product_id], 10
        )

    def test_setup_products_qty_array_to_final_products_qty_map(self):

        mocked_get_inventory_ingredient_by_ingredient_id_mock = Mock(
            wraps=get_inventory_ingredient_by_ingredient_id_mock
        )
        mocked_get_product_ingredient_by_product_id_mock = Mock(
            wraps=get_product_ingredient_by_product_id_mock
        )
        reduce_products_qty_array_to_final_products_qty_map = (
            setup_products_qty_array_to_final_products_qty_map(
                mocked_get_inventory_ingredient_by_ingredient_id_mock,
                mocked_get_product_ingredient_by_product_id_mock,
            )
        )
        product_possible_qty_quantity = (
            reduce_products_qty_array_to_final_products_qty_map([1])
        )
        self.assertEqual(product_possible_qty_quantity[1], 10)
        mocked_get_inventory_ingredient_by_ingredient_id_mock.assert_called_with(1)
        mocked_get_product_ingredient_by_product_id_mock.assert_called_with(1)
