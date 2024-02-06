from unittest import mock

from src.api.controllers.product_controller import ProductController
from src.lib.repositories.impl_v2.product_repository_impl import ProductRepositoryImpl
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import build_product, build_products


class ProductRepositoryControllerIntegrationTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.product_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.product_repository = mock.Mock(
            wraps=ProductRepositoryImpl(self.mocked_sqlalchemy_engine)
        )
        self.mocked_creation_session_path.start()

        self.product_controller = ProductController(self.product_repository)

    def test_add_product_to_repository_using_controller(self):

        product = build_product()

        self.product_controller.add(product)
        self.product_repository.add.assert_called_with(product)

    def test_get_product_from_repository_using_controller(self):

        products = build_products(count=3)

        self.product_controller.add(products[0])
        self.product_controller.add(products[1])
        self.product_controller.add(products[2])
        self.product_repository.get_by_id.return_value = products[1]
        found_product1 = self.product_controller.get_by_id(1)

        self.product_repository.get_by_id.assert_called_with(1)
        self.assertEqual(found_product1.id, 1)

    def test_get_all_products_from_repository_using_controller(self):

        products_to_insert = build_products(count=4)

        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])
        self.product_controller.add(products_to_insert[2])
        self.product_controller.add(products_to_insert[3])
        self.product_repository.get_all.return_value = products_to_insert
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
        self.product_repository.get_all.return_value = []
        products = self.product_controller.get_all()
        self.product_repository.get_all.assert_called_with()
        self.assertEqual(products, [])

    def test_delete_an_product_from_repository_using_controller(self):

        products_to_insert = build_products(count=4)

        product_to_delete = build_product()
        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])
        self.product_controller.add(products_to_insert[2])
        self.product_controller.add(products_to_insert[3])

        self.product_controller.delete_by_id(3, product_to_delete)
        self.product_repository.get_all.return_value = [
            products_to_insert[0],
            products_to_insert[1],
            products_to_insert[3],
        ]
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

    def test_update_product_from_repository_using_controller(self):

        products_to_insert = build_products(count=2)

        self.product_controller.add(products_to_insert[0])
        self.product_controller.add(products_to_insert[1])

        product_to_update = build_product(description="updated-description")

        self.product_controller.update_by_id(2, product_to_update)
        self.product_repository.get_by_id.return_value = product_to_update
        updated_product = self.product_controller.get_by_id(2)
        self.product_repository.get_all.return_value = products_to_insert
        products = self.product_controller.get_all()

        self.product_repository.update_by_id.assert_called_once_with(
            2, product_to_update
        )

        self.assertEqual(len(products), 2)
        self.assertEqual(updated_product.description, product_to_update.description)
