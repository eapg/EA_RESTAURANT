from unittest import mock

from src.constants import audit
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import product_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class ProductRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.product_repository = product_repository_impl.ProductRepositoryImpl()

    def test_add_product_successfully(self):
        product_1 = mapping_orm_fixtures.build_product(
            name="product_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )

        self.product_repository.add(product_1)
        self.product_repository.session.add.assert_called_with(product_1)

    def test_get_product_successfully(self):
        product_1 = mapping_orm_fixtures.build_product(
            name="product_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=product_1)
            .get_mocked_query()
        )
        product_1.id = 5
        result = self.product_repository.get_by_id(product_1.id)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Product)
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
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(result, product_1)

    def test_get_all_successfully(self):
        products = mapping_orm_fixtures.build_products(count=4)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=products)
            .get_mocked_query()
        )

        returned_products = self.product_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Product)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(products, returned_products)

    @mock.patch("src.lib.repositories.impl_v2.product_repository_impl.datetime")
    def test_delete_by_id_successfully(self, mocked_datetime):
        product_1 = mapping_orm_fixtures.build_product(
            name="product_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )

        product_1.updated_by = 2

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        product_1.id = 5
        self.product_repository.delete_by_id(product_1.id, product_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Product)

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
                sqlalchemy_orm_mapping.Product.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.Product.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.Product.updated_by: product_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        product_1 = mapping_orm_fixtures.build_product(
            name="product_1", entity_status=audit.Status.ACTIVE.value, create_by=1
        )
        product_1.id = 5
        product_to_be_updated = mapping_orm_fixtures.build_product()
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=product_to_be_updated)
            .get_mocked_query()
        )

        self.product_repository.update_by_id(product_1.id, product_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Product)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            product_1.id,
        )

        self.product_repository.session.add.assert_called_with(product_to_be_updated)
