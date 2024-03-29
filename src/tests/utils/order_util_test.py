import unittest
from unittest.mock import Mock

from src.constants.cooking_type import CookingType
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_order_detail,
    build_chef,
    build_order,
    build_product_ingredient,
)
from src.utils.order_util import (
    array_chef_to_chef_assigned_orders_map_reducer,
    compute_order_estimated_time,
    order_products_validation_reducer,
    setup_validated_orders_map,
    validated_orders_reducer,
)


def get_final_product_qty_by_product_ids_mock(product_ids):
    products_qty = {1: 10, 2: 20, 3: 30}
    product_qty_by_product_ids = {}
    for product_id in product_ids:
        product_qty_by_product_ids[product_id] = products_qty[product_id]
    return product_qty_by_product_ids


def get_order_detail_by_order_id_mock(order_id):

    order_detail_1 = build_order_detail(
        order_detail_id=1, order_id=1, product_id=1, quantity=2
    )
    order_detail_2 = build_order_detail(
        order_detail_id=2, order_id=2, product_id=2, quantity=2
    )
    order_details = {1: order_detail_1, 2: order_detail_2}
    return [order_details[order_id]]


@unittest.skip("Deprecated")
class TestOrderUtil(unittest.TestCase):
    def test_array_chef_to_chef_assigned_orders_map_reducer(self):

        chef_principal = build_chef(chef_id=1, name="Elido p", skill=5)

        order_1 = build_order(assigned_chef_id=chef_principal.id)
        order_2 = build_order(assigned_chef_id=None)
        order_3 = build_order(assigned_chef_id=chef_principal.id)

        orders = [order_1, order_2, order_3]

        chefs_with_assigned_orders_map = {}

        chefs_with_assigned_orders_map = array_chef_to_chef_assigned_orders_map_reducer(
            chefs_with_assigned_orders_map, chef_principal.id, orders
        )
        self.assertEqual(chefs_with_assigned_orders_map[1], [order_1, order_3])

    def test_order_products_validation_reducer(self):

        quantity_product_that_can_be_made_map = {1: 10}
        order_detail_1 = build_order_detail(order_detail_id=1, quantity=3, product_id=1)

        order_products_validation = order_products_validation_reducer(
            [], order_detail_1, quantity_product_that_can_be_made_map
        )
        self.assertTrue(order_products_validation[0])

    def test_validated_orders_reducer(self):

        order_1 = build_order(order_id=1)
        order_products_availability_validation = [True, True, True]
        validated_orders_map = validated_orders_reducer(
            {}, order_1, order_products_availability_validation
        )
        self.assertTrue(validated_orders_map[order_1.id])

    def test_setup_validated_orders_map(self):
        order_1 = build_order(order_id=1)
        mocked_get_final_product_qty_by_product_ids_mock = Mock(
            wraps=get_final_product_qty_by_product_ids_mock
        )
        mocked_get_order_detail_by_order_id_mock = Mock(
            wraps=get_order_detail_by_order_id_mock
        )
        reduce_validate_orders_map = setup_validated_orders_map(
            mocked_get_final_product_qty_by_product_ids_mock,
            mocked_get_order_detail_by_order_id_mock,
        )
        validated_orders_map = reduce_validate_orders_map([order_1])

        self.assertTrue(validated_orders_map[order_1.id])
        mocked_get_final_product_qty_by_product_ids_mock.assert_called_with([1])
        mocked_get_order_detail_by_order_id_mock.assert_called_with(1)

    def test_computed_order_estimated_time(self):

        chef_1 = build_chef(chef_id=1, skill=2)
        product_ingredient_1 = build_product_ingredient(
            product_ingredient_id=1, quantity=3
        )
        product_ingredient_1.cooking_type = CookingType.ADDING.name
        product_ingredient_2 = build_product_ingredient(
            product_ingredient_id=2, quantity=3
        )
        product_ingredient_2.cooking_type = CookingType.ADDING.name
        order_ingredients_list = [
            product_ingredient_1,
            product_ingredient_2,
        ]
        preparation_time = compute_order_estimated_time(order_ingredients_list, chef_1)
        self.assertEqual(preparation_time, 6)
