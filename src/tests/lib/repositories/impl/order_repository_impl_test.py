import unittest
from unittest import mock

from src.lib.repositories.impl.order_detail_repository_impl import (
    OrderDetailRepositoryImpl,
)
from src.lib.repositories.impl.order_repository_impl import OrderRepositoryImpl
from src.lib.repositories.impl.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.order_fixture import build_order, build_orders
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient
from src.tests.utils.fixtures.product_fixture import build_product
from src.constants.order_status import OrderStatus


class OrderRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_successfully(self):
        order = build_order()
        order_repository = OrderRepositoryImpl()

        self.assertIsNone(order.id)

        order_repository.add(order)

        self.assertEqual(order.id, 1)

    def test_get_order_successfully(self):
        orders = build_orders(count=3)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders[0])
        order_repository.add(orders[1])
        order_repository.add(orders[2])

        found_order3 = order_repository.get_by_id(3)

        self.assertEqual(found_order3.id, 3)

    def test_get_throws_key_error_for_non_existing_order(self):
        order1 = build_order()

        order_repository = OrderRepositoryImpl()

        order_repository.add(order1)

        self.assertRaises(KeyError, order_repository.get_by_id, 2)

    def test_get_all_orders_successfully(self):
        orders_to_insert = build_orders(count=5)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])
        order_repository.add(orders_to_insert[2])
        order_repository.add(orders_to_insert[3])
        order_repository.add(orders_to_insert[4])

        orders = order_repository.get_all()

        self.assertEqual(
            orders,
            [
                orders_to_insert[0],
                orders_to_insert[1],
                orders_to_insert[2],
                orders_to_insert[3],
                orders_to_insert[4],
            ],
        )

    def test_get_all_orders_empty_successfully(self):
        order_repository = OrderRepositoryImpl()

        orders = order_repository.get_all()

        self.assertEqual(orders, [])

    def test_delete_an_order_successfully(self):
        orders_to_insert = build_orders(count=3)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])
        order_repository.add(orders_to_insert[2])

        order_repository.delete_by_id(2)

        orders = order_repository.get_all()

        self.assertEqual(orders, [orders_to_insert[0], orders_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_orders(self):
        order_repository = OrderRepositoryImpl()

        self.assertRaises(KeyError, order_repository.delete_by_id, 2)

    def test_update_order_successfully(self):
        orders_to_insert = build_orders(count=2)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])

        order_to_update = build_order(order_details=build_order_detail())

        order_repository.update_by_id(2, order_to_update)
        updated_order = order_repository.get_by_id(2)
        orders = order_repository.get_all()

        self.assertEqual(len(orders), 2)
        self.assertEqual(updated_order.order_details, order_to_update.order_details)

    def test_get_orders_to_process(self):
        order_1 = build_order()
        order_2 = build_order()
        order_3 = build_order(status=OrderStatus.COMPLETED)

        order_repository = OrderRepositoryImpl()
        order_repository.add(order_1)
        order_repository.add(order_2)
        order_repository.add(order_3)

        self.assertEqual(len(order_repository.get_orders_to_process()), 2)

    def test_get_order_ingredients_by_order_id(self):
        product_ingredient_repository = mock.Mock(
            wraps=ProductIngredientRepositoryImpl()
        )
        order_detail_repository = mock.Mock(wraps=OrderDetailRepositoryImpl())
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")
        ingredient_2 = build_ingredient(ingredient_id=2, name="ingredient_2")
        product_1 = build_product(product_id=1, name="product_1")
        product_ingredient_1 = build_product_ingredient(
            id=1, product_id=product_1.id, ingredient_id=ingredient_1.id, quantity=2
        )
        product_ingredient_repository.add(product_ingredient_1)

        product_ingredient_2 = build_product_ingredient(
            id=2, product_id=product_1.id, ingredient_id=ingredient_2.id, quantity=2
        )
        product_ingredient_repository.add(product_ingredient_2)

        order_1 = build_order(order_id=1)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_1.id, product_id=product_1.id, quantity=2
        )
        order_detail_repository.add(order_detail_1)
        order_repository = OrderRepositoryImpl(
            order_detail_repository, product_ingredient_repository
        )
        order_ingredients = order_repository.get_order_ingredients_by_order_id(
            order_1.id
        )
        product_ingredient_repository.get_product_ingredients_by_product_ids.assert_called_with(
            [product_1.id, product_1.id]
        )
        order_detail_repository.get_by_order_id.assert_called_with(order_1.id)

        self.assertEqual(
            order_ingredients, [product_ingredient_1, product_ingredient_2]
        )
