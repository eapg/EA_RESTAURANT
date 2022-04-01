import unittest

from src.lib.repositories.impl.product_repository_impl import ProductRepositoryImpl
from src.tests.utils.fixtures.product_fixture import build_product, build_products


class ProductRepositoryImplTestCase(unittest.TestCase):
    def test_add_product_successfully(self):
        product = build_product()
        product_repository = ProductRepositoryImpl()

        self.assertIsNone(product.id)

        product_repository.add(product)

        self.assertEqual(product.id, 1)

    def test_get_product_successfully(self):
        products = build_products(count=3)

        product_repository = ProductRepositoryImpl()

        product_repository.add(products[0])
        product_repository.add(products[1])
        product_repository.add(products[2])

        found_product3 = product_repository.get_by_id(3)

        self.assertEqual(found_product3.id, 3)

    def test_get_throws_key_error_for_non_existing_product(self):
        product1 = build_product()

        product_repository = ProductRepositoryImpl()

        product_repository.add(product1)

        self.assertRaises(KeyError, product_repository.get_by_id, 2)

    def test_get_all_products_successfully(self):
        products_to_insert = build_products(count=5)

        product_repository = ProductRepositoryImpl()

        product_repository.add(products_to_insert[0])
        product_repository.add(products_to_insert[1])
        product_repository.add(products_to_insert[2])
        product_repository.add(products_to_insert[3])
        product_repository.add(products_to_insert[4])

        products = product_repository.get_all()

        self.assertEqual(
            products,
            [
                products_to_insert[0],
                products_to_insert[1],
                products_to_insert[2],
                products_to_insert[3],
                products_to_insert[4],
            ],
        )

    def test_get_all_products_empty_successfully(self):
        product_repository = ProductRepositoryImpl()

        products = product_repository.get_all()

        self.assertEqual(products, [])

    def test_delete_an_product_successfully(self):
        products_to_insert = build_products(count=3)

        product_repository = ProductRepositoryImpl()

        product_repository.add(products_to_insert[0])
        product_repository.add(products_to_insert[1])
        product_repository.add(products_to_insert[2])

        product_repository.delete_by_id(2)

        products = product_repository.get_all()

        self.assertEqual(products, [products_to_insert[0], products_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_products(self):
        product_repository = ProductRepositoryImpl()

        self.assertRaises(KeyError, product_repository.delete_by_id, 2)

    def test_update_product_successfully(self):
        products_to_insert = build_products(count=2)

        product_repository = ProductRepositoryImpl()

        product_repository.add(products_to_insert[0])
        product_repository.add(products_to_insert[1])

        product_to_update = build_product(name="updated-name")

        product_repository.update_by_id(2, product_to_update)
        updated_product = product_repository.get_by_id(2)
        products = product_repository.get_all()

        self.assertEqual(len(products), 2)
        self.assertEqual(updated_product.name, product_to_update.name)
