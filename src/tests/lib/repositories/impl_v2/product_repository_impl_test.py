from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import Product
from src.lib.repositories.impl_v2.product_repository_impl import ProductRepositoryImpl
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import build_product, build_products


class ProductRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.product_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.product_repository = ProductRepositoryImpl(self.mocked_sqlalchemy_engine)
        self.mocked_creation_session_path.start()

    def test_add_product_successfully(self):
        product_1 = build_product(
            name="product_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        self.product_repository.add(product_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(product_1)

    def test_get_product_successfully(self):
        product_1 = build_product(
            name="product_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=product_1)
            .get_mocked_query()
        )
        product_1.id = 5
        result = self.product_repository.get_by_id(product_1.id)

        mocked_query.assert_called_with(Product)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_1.id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(result, product_1)

    def test_get_all_successfully(self):
        products = build_products(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=products)
            .get_mocked_query()
        )

        returned_products = self.product_repository.get_all()

        mocked_query.assert_called_with(Product)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(products, returned_products)

    @mock.patch("src.lib.repositories.impl_v2.product_repository_impl.datetime")
    def test_delete_by_id_successfully(self, mocked_datetime):
        product_1 = build_product(
            name="product_1", entity_status=Status.ACTIVE.value, create_by=1
        )

        product_1.updated_by = 2

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        product_1.id = 5
        self.product_repository.delete_by_id(product_1.id, product_1)

        mocked_query.assert_called_with(Product)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                Product.entity_status: Status.DELETED.value,
                Product.updated_date: mocked_datetime.now(),
                Product.updated_by: product_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        product_1 = build_product(
            name="product_1", entity_status=Status.ACTIVE.value, create_by=1
        )
        product_1.id = 5
        product_to_be_updated = build_product()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=product_to_be_updated)
            .get_mocked_query()
        )

        self.product_repository.update_by_id(product_1.id, product_1)

        mocked_query.assert_called_with(Product)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_1.id,
        )

        self.mocked_sqlalchemy_session.add.assert_called_with(product_to_be_updated)
