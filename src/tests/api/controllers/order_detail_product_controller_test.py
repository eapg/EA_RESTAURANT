import unittest
from unittest import mock

from src.api.controllers.order_detail_product_controller import \
    OrderDetailProductController
from src.tests.utils.fixtures.order_detail_product_fixture import (
    build_order_detail_product, build_order_detail_products)


class OrderDetailProductRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_detail_product_repository = mock.Mock()
        self.order_detail_product_controller = OrderDetailProductController(
            self.order_detail_product_repository
        )

    def test_add_order_detail_product_successfully(self):
        order_detail_product = build_order_detail_product()

        self.order_detail_product_controller.add(order_detail_product)

        self.order_detail_product_repository.add.assert_called_with(
            order_detail_product
        )

    def test_get_order_detail_product_successfully(self):
        order_detail_product = build_order_detail_product()

        self.order_detail_product_repository.get_by_id.return_value = (
            order_detail_product
        )

        expected_order_detail_product = self.order_detail_product_controller.get_by_id(
            order_detail_product.id
        )

        self.order_detail_product_repository.get_by_id.assert_called_with(
            order_detail_product.id
        )
        self.assertEqual(expected_order_detail_product.id, order_detail_product.id)

    def test_get_all_order_detail_products_successfully(self):
        order_detail_products = build_order_detail_products(count=3)

        self.order_detail_product_repository.get_all.return_value = (
            order_detail_products
        )

        expected_order_detail_products = self.order_detail_product_controller.get_all()

        self.order_detail_product_repository.get_all.assert_called()
        self.assertEqual(expected_order_detail_products, order_detail_products)
        self.assertEqual(len(expected_order_detail_products), 3)

    def test_delete_an_order_detail_product_successfully(self):
        self.order_detail_product_controller.delete_by_id(2)

        self.order_detail_product_repository.delete_by_id.assert_called_with(2)

    def test_update_an_order_detail_product_successfully(self):
        order_detail_product = build_order_detail_product()

        self.order_detail_product_controller.update_by_id(1, order_detail_product)

        self.order_detail_product_repository.update_by_id.assert_called_with(
            1, order_detail_product
        )
