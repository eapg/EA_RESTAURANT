import unittest
from unittest import mock

from src.api.controllers.product_controller import ProductController
from src.tests.utils.fixtures.product_fixture import build_product, build_products


class ProductRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.product_repository = mock.Mock()
        self.product_controller = ProductController(self.product_repository)

    def test_add_product_successfully(self):
        product = build_product()

        self.product_controller.add(product)

        self.product_repository.add.assert_called_with(product)

    def test_get_product_successfully(self):
        product = build_product()

        self.product_repository.get_by_id.return_value = product

        expected_product = self.product_controller.get_by_id(product.id)

        self.product_repository.get_by_id.assert_called_with(product.id)
        self.assertEqual(expected_product.id, product.id)

    def test_get_all_products_successfully(self):
        products = build_products(count=3)

        self.product_repository.get_all.return_value = products

        expected_products = self.product_controller.get_all()

        self.product_repository.get_all.assert_called()
        self.assertEqual(expected_products, products)
        self.assertEqual(len(expected_products), 3)

    def test_delete_an_product_successfully(self):
        self.product_controller.delete_by_id(2)

        self.product_repository.delete_by_id.assert_called_with(2)

    def test_update_an_product_successfully(self):
        product = build_product()

        self.product_controller.update_by_id(1, product)

        self.product_repository.update_by_id.assert_called_with(1, product)
