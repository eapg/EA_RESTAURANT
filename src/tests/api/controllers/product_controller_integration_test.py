import unittest
from unittest import mock

from src.api.controllers import product_controller
from src.constants import audit
from src.lib.repositories.impl import product_repository_impl
from src.tests.utils.fixtures import product_fixture


class ProductRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = mock.Mock(
            wraps=product_repository_impl.ProductRepositoryImpl()
        )
        self.product_controller = product_controller.ProductController(
            self.product_repository
        )

    def test_add_product_to_repository_using_controller(self):
        product = product_fixture.build_product()

        self.product_controller.add(product)
        self.product_repository.add.assert_called_with(product)
        self.assertEqual(product.id, 1)

    def test_get_product_from_repository_using_controller(self):
        products = product_fixture.build_products(count=3)

        self.product_controller.add(products[0])
        self.product_controller.add(products[1])
        self.product_controller.add(products[2])

        found_product3 = self.product_controller.get_by_id(3)

        self.product_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_product3.id, 3)

    def test_get_throws_key_error_for_non_existing_product(self):
        product1 = product_fixture.build_product()

        self.product_controller.add(product1)

        self.assertRaises(KeyError, self.product_controller.get_by_id, 2)
        self.product_repository.get_by_id.assert_called_with(2)

    def test_get_all_products_from_repository_using_controller(self):

        products_to_insert = product_fixture.build_products(count=4)

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
        products_to_insert = product_fixture.build_products(count=4)
        product_to_delete = product_fixture.build_product(
            entity_status=audit.Status.DELETED
        )
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
        product_to_delete = product_fixture.build_product(
            entity_status=audit.Status.DELETED
        )
        self.assertRaises(
            KeyError, self.product_controller.delete_by_id, 3, product_to_delete
        )
        self.product_repository.delete_by_id.assert_called_with(3, product_to_delete)

    def test_update_product_from_repository_using_controller(self):
        products_to_insert = product_fixture.build_products(count=2)

        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])

        product_to_update = product_fixture.build_product(
            description="updated-description"
        )

        self.product_controller.update_by_id(2, product_to_update)
        updated_product = self.product_controller.get_by_id(2)
        products = self.product_controller.get_all()

        self.product_repository.update_by_id.assert_called_once_with(
            2, product_to_update
        )

        self.assertEqual(len(products), 2)
        self.assertEqual(updated_product.description, product_to_update.description)
