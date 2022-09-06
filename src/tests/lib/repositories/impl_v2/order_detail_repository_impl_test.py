from unittest import mock

from src.constants import audit
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import order_detail_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class OrderDetailRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.order_detail_repository = (
            order_detail_repository_impl.OrderDetailRepositoryImpl()
        )

    def test_add_order_detail_successfully(self):
        order_detail_1 = mapping_orm_fixtures.build_order_detail()

        self.order_detail_repository.add(order_detail_1)
        self.order_detail_repository.session.add.assert_called_with(order_detail_1)

    def test_get_order_detail_successfully(self):
        order_detail_1 = mapping_orm_fixtures.build_order_detail()

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=order_detail_1)
            .get_mocked_query()
        )
        order_detail_1.id = 5
        result = self.order_detail_repository.get_by_id(order_detail_1.id)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderDetail)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_detail_1.id,
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
        self.assertEqual(result, order_detail_1)

    def test_get_all_order_details_successfully(self):
        order_details = mapping_orm_fixtures.build_order_details(count=4)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=order_details)
            .get_mocked_query()
        )

        returned_order_details = self.order_detail_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderDetail)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(order_details, returned_order_details)

    @mock.patch("src.lib.repositories.impl_v2.order_detail_repository_impl.datetime")
    def test_delete_an_order_detail_successfully(self, mocked_datetime):
        order_detail_1 = mapping_orm_fixtures.build_order_detail()
        order_detail_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        order_detail_1.id = 5
        self.order_detail_repository.delete_by_id(order_detail_1.id, order_detail_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderDetail)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_detail_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.OrderDetail.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.OrderDetail.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.OrderDetail.updated_by: order_detail_1.updated_by,
            }
        )

    def test_update_order_detail_successfully(self):
        order_detail_1 = mapping_orm_fixtures.build_order_detail()
        order_detail_1.id = 5
        order_detail_to_be_updated = mapping_orm_fixtures.build_order_detail()
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_detail_to_be_updated)
            .get_mocked_query()
        )

        self.order_detail_repository.update_by_id(order_detail_1.id, order_detail_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderDetail)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_detail_1.id,
        )

        self.order_detail_repository.session.add.assert_called_with(
            order_detail_to_be_updated
        )

    def test_get_by_order_id_successfully(self):
        order_1 = sqlalchemy_orm_mapping.Order()
        order_1.id = 2
        order_detail_1 = mapping_orm_fixtures.build_order_detail(order_id=order_1.id)
        order_detail_2 = mapping_orm_fixtures.build_order_detail(order_id=order_1.id)

        order_details_of_order_1 = [order_detail_1, order_detail_2]

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=order_details_of_order_1)
            .get_mocked_query()
        )

        order_details_returned = self.order_detail_repository.get_by_order_id(
            order_1.id
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderDetail)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "order_id",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            order_1.id,
        )
        self.assertEqual(order_details_returned, order_details_of_order_1)
