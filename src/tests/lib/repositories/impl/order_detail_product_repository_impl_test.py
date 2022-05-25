import unittest

from src.lib.repositories.impl.order_detail_product_repository_impl import (
    OrderDetailProductRepositoryImpl,
)
from src.tests.utils.fixtures.order_detail_product_fixture import (
    build_order_detail_product,
    build_order_detail_products,
)
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.product_fixture import build_product


class OrderDetailProductRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_detail_product_successfully(self):
        order_detail_product = build_order_detail_product()
        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        self.assertIsNone(order_detail_product.id)

        order_detail_product_repository.add(order_detail_product)

        self.assertEqual(order_detail_product.id, 1)

    def test_get_order_detail_product_successfully(self):
        order_detail_products = build_order_detail_products(count=3)

        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_product_repository.add(order_detail_products[0])
        order_detail_product_repository.add(order_detail_products[1])
        order_detail_product_repository.add(order_detail_products[2])

        found_order_detail_product3 = order_detail_product_repository.get_by_id(3)

        self.assertEqual(found_order_detail_product3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_detail_product(self):
        order_detail_product1 = build_order_detail_product()

        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_product_repository.add(order_detail_product1)

        self.assertRaises(KeyError, order_detail_product_repository.get_by_id, 2)

    def test_get_all_order_detail_products_successfully(self):
        order_detail_products_to_insert = build_order_detail_products(count=5)

        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_product_repository.add(order_detail_products_to_insert[0])
        order_detail_product_repository.add(order_detail_products_to_insert[1])
        order_detail_product_repository.add(order_detail_products_to_insert[2])
        order_detail_product_repository.add(order_detail_products_to_insert[3])
        order_detail_product_repository.add(order_detail_products_to_insert[4])

        order_detail_products = order_detail_product_repository.get_all()

        self.assertEqual(
            order_detail_products,
            [
                order_detail_products_to_insert[0],
                order_detail_products_to_insert[1],
                order_detail_products_to_insert[2],
                order_detail_products_to_insert[3],
                order_detail_products_to_insert[4],
            ],
        )

    def test_get_all_order_detail_products_empty_successfully(self):
        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_products = order_detail_product_repository.get_all()

        self.assertEqual(order_detail_products, [])

    def test_delete_an_order_detail_product_successfully(self):
        order_detail_products_to_insert = build_order_detail_products(count=3)

        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_product_repository.add(order_detail_products_to_insert[0])
        order_detail_product_repository.add(order_detail_products_to_insert[1])
        order_detail_product_repository.add(order_detail_products_to_insert[2])

        order_detail_product_repository.delete_by_id(2)

        order_detail_products = order_detail_product_repository.get_all()

        self.assertEqual(
            order_detail_products,
            [order_detail_products_to_insert[0], order_detail_products_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_order_detail_products(self):
        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        self.assertRaises(KeyError, order_detail_product_repository.delete_by_id, 2)

    def test_update_order_detail_product_successfully(self):
        order_detail_products_to_insert = build_order_detail_products(count=2)

        order_detail_product_repository = OrderDetailProductRepositoryImpl()

        order_detail_product_repository.add(order_detail_products_to_insert[0])
        order_detail_product_repository.add(order_detail_products_to_insert[1])

        order_detail_product_to_update = build_order_detail_product(quantity=5)

        order_detail_product_repository.update_by_id(2, order_detail_product_to_update)
        updated_order_detail_product = order_detail_product_repository.get_by_id(2)
        order_detail_products = order_detail_product_repository.get_all()

        self.assertEqual(len(order_detail_products), 2)
        self.assertEqual(
            updated_order_detail_product.quantity,
            order_detail_product_to_update.quantity,
        )

    def test_get_by_order_detail_id(self):
        order_detail_1 = build_order_detail(order_detail_id=1)
        product_1 = build_product(product_id=1, name="test product 1")
        product_2 = build_product(product_id=2, name="test product 2")
        order_detail_product_1 = build_order_detail_product(
            order_detail_id=order_detail_1.id, product=product_1, quantity=2
        )
        order_detail_product_2 = build_order_detail_product(
            order_detail_id=order_detail_1.id, product=product_2, quantity=3
        )
        order_detail_product_repository = OrderDetailProductRepositoryImpl()
        order_detail_product_repository.add(order_detail_product_1)
        order_detail_product_repository.add(order_detail_product_2)

        order_detail_products_by_order_detail_id = (
            order_detail_product_repository.get_by_order_detail_id(order_detail_1.id)
        )
        self.assertEqual(len(order_detail_products_by_order_detail_id), 2)
        self.assertEqual(
            order_detail_products_by_order_detail_id,
            [order_detail_product_1, order_detail_product_2],
        )
