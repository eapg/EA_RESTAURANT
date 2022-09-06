from unittest import mock

from src.constants import audit, order_status
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import order_status_history_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class OrderStatusHistoryRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

    def test_add_order_status_history_successfully(self):
        order_status_history_1 = mapping_orm_fixtures.build_order_status_history()

        self.order_status_history_repository.add(order_status_history_1)
        self.order_status_history_repository.session.add.assert_called_with(
            order_status_history_1
        )

    def test_get_order_status_history_successfully(self):
        order_status_history_1 = mapping_orm_fixtures.build_order_status_history()

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=order_status_history_1)
            .get_mocked_query()
        )
        order_status_history_1.id = 5
        result = self.order_status_history_repository.get_by_id(
            order_status_history_1.id
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderStatusHistory)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_status_history_1.id,
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
        self.assertEqual(result, order_status_history_1)

    def test_get_all_successfully(self):
        order_status_histories = mapping_orm_fixtures.build_order_status_histories(
            count=4
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=order_status_histories)
            .get_mocked_query()
        )

        returned_order_status_histories = self.order_status_history_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderStatusHistory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(order_status_histories, returned_order_status_histories)

    @mock.patch(
        "src.lib.repositories.impl_v2.order_status_history_repository_impl.datetime"
    )
    def test_delete_by_id_successfully(self, mocked_datetime):
        order_status_history_1 = mapping_orm_fixtures.build_order_status_history()
        order_status_history_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        order_status_history_1.id = 5
        self.order_status_history_repository.delete_by_id(
            order_status_history_1.id, order_status_history_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderStatusHistory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_status_history_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.OrderStatusHistory.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.OrderStatusHistory.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.OrderStatusHistory.updated_by: order_status_history_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        order_status_history_1 = mapping_orm_fixtures.build_order_status_history()
        order_status_history_1.id = 5
        order_status_history_to_be_updated = (
            mapping_orm_fixtures.build_order_status_history()
        )
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_status_history_to_be_updated)
            .get_mocked_query()
        )

        self.order_status_history_repository.update_by_id(
            order_status_history_1.id, order_status_history_1
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderStatusHistory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_status_history_1.id,
        )

        self.order_status_history_repository.session.add.assert_called_with(
            order_status_history_to_be_updated
        )

    def test_get_by_order_id(self):
        order_1 = sqlalchemy_orm_mapping.Order()
        order_1.id = 2
        order_status_history_1 = mapping_orm_fixtures.build_order_status_history(
            order_id=2
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=[order_status_history_1])
            .get_mocked_query()
        )

        order_status_histories_returned = (
            self.order_status_history_repository.get_by_order_id(order_1.id)
        )
        mocked_query.assert_called_with(sqlalchemy_orm_mapping.OrderStatusHistory)

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
        self.assertEqual(order_status_histories_returned, [order_status_history_1])

    @mock.patch(
        "src.lib.repositories.impl_v2.order_status_history_repository_impl.sql.func"
    )
    def test_set_next_status_history_by_order_id(self, mocked_func):
        order_1 = sqlalchemy_orm_mapping.Order()
        order_1.id = 3

        order_status_history_to_return = (
            mapping_orm_fixtures.build_order_status_history(order_id=order_1.id)
        )

        query_last_order_status_id = (
            sqlalchemy_mock_builder.QueryMock().query().first(return_value=(3,))
        ).get_mocked_query()

        query_last_order_status_history = (
            sqlalchemy_mock_builder.QueryMock()
            .query()
            .filter()
            .filter()
            .filter()
            .first(return_value=order_status_history_to_return)
        ).get_mocked_query()

        def mock_query_side_effect(t):
            return (
                query_last_order_status_id.return_value
                if t == mocked_func.max()
                else query_last_order_status_history.return_value
            )

        sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session).query(
            side_effect_fn=mock_query_side_effect
        )

        self.order_status_history_repository.set_next_status_history_by_order_id(
            order_1.id, order_status.OrderStatus.CANCELLED.name
        )

        self.assertEqual(
            query_last_order_status_history.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "entity_status",
        )

        self.assertEqual(
            query_last_order_status_history.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            query_last_order_status_history.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left,
            sqlalchemy_orm_mapping.OrderStatusHistory.order_id,
        )

        self.assertEqual(
            query_last_order_status_history.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            order_1.id,
        )
