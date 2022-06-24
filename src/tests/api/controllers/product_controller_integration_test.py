import unittest
from unittest import mock
from src.constants.audit import Status
from src.api.controllers.product_controller import ProductController
from src.lib.repositories.impl.product_repository_impl import ProductRepositoryImpl
from src.tests.utils.fixtures.product_fixture import build_product, build_products


class ProductRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = mock.Mock(wraps=ProductRepositoryImpl())
        self.product_controller = ProductController(self.product_repository)

    def test_add_product_to_repository_using_controller(self):
        product = build_product()

        self.assertIsNone(product.id)

        self.product_controller.add(product)
        self.product_repository.add.assert_called_with(product)

    def test_get_product_from_repository_using_controller(self):
        products = build_products(count=3)

        self.product_controller.add(products[0])
        self.product_controller.add(products[1])
        self.product_controller.add(products[2])

        found_product3 = self.product_controller.get_by_id(3)

        self.product_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_product3.id, 3)

    def test_get_throws_key_error_for_non_existing_product(self):
        product1 = build_product()

        self.product_controller.add(product1)

        self.assertRaises(KeyError, self.product_controller.get_by_id, 2)
        self.product_repository.get_by_id.assert_called_with(2)

    def test_get_all_products_from_repository_using_controller(self):

        products_to_insert = build_products(count=4)

        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])
        self.product_controller.add(products_to_insert[2])
        self.product_controller.add(products_to_insert[3])

        products = self.product_controller.get_all()

        self.product_repository.get_all.assert_called_with()

        self.assertEqual(
            products,
            [
                products_to_insert[0],
                products_to_insert[1],
                products_to_insert[2],
                products_to_insert[3],
            ],
        )

    def test_get_all_products_empty_from_repository_through_controller(self):
        products = self.product_controller.get_all()
        self.product_repository.get_all.assert_called_with()
        self.assertEqual(products, [])

    def test_delete_an_product_from_repository_using_controller(self):
        products_to_insert = build_products(count=4)
        product_to_delete = build_product(entity_status=Status.DELETED)
        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])
        self.product_controller.add(products_to_insert[2])
        self.product_controller.add(products_to_insert[3])

        self.product_controller.delete_by_id(3, product_to_delete)
        products = self.product_controller.get_all()

        self.product_repository.delete_by_id.assert_called_once_with(
            3, product_to_delete
        )

        self.assertEqual(
            products,
            [
                products_to_insert[0],
                products_to_insert[1],
                products_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_products(self):
        product_to_delete = build_product(entity_status=Status.DELETED)
        self.assertRaises(
            KeyError, self.product_controller.delete_by_id, 3, product_to_delete
        )
        self.product_repository.delete_by_id.assert_called_with(3, product_to_delete)

    def test_update_product_from_repository_using_controller(self):
        products_to_insert = build_products(count=2)

        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])

        product_to_update = build_product(description="updated-description")

        self.product_controller.update_by_id(2, product_to_update)
        updated_product = self.product_controller.get_by_id(2)
        products = self.product_controller.get_all()

        self.product_repository.update_by_id.assert_called_once_with(
            2, product_to_update
        )

        self.assertEqual(len(products), 2)
        self.assertEqual(updated_product.description, product_to_update.description)
