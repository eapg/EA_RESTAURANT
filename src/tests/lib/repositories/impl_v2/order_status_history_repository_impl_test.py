from unittest import mock

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.sqlalchemy_orm_mapping import OrderStatusHistory, Order
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_order_status_history,
    build_order_status_histories,
)
from src.lib.repositories.impl_v2.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class OrderStatusHistoryRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.order_status_history_repository = OrderStatusHistoryRepositoryImpl(
            self.mocked_sqlalchemy_session
        )

    def test_add_order_status_history_successfully(self):
        order_status_history_1 = build_order_status_history()

        self.order_status_history_repository.add(order_status_history_1)
        self.order_status_history_repository.session.add.assert_called_with(
            order_status_history_1
        )

    def test_get_order_status_history_successfully(self):
        order_status_history_1 = build_order_status_history()

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
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

        mocked_query.assert_called_with(OrderStatusHistory)
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
            Status.ACTIVE.value,
        )
        self.assertEqual(result, order_status_history_1)

    def test_get_all_successfully(self):
        order_status_histories = build_order_status_histories(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=order_status_histories)
            .get_mocked_query()
        )

        returned_order_status_histories = self.order_status_history_repository.get_all()

        mocked_query.assert_called_with(OrderStatusHistory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(order_status_histories, returned_order_status_histories)

    @mock.patch(
        "src.lib.repositories.impl_v2.order_status_history_repository_impl.datetime"
    )
    def test_delete_by_id_successfully(self, mocked_datetime):
        order_status_history_1 = build_order_status_history()
        order_status_history_1.updated_by = 1

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        order_status_history_1.id = 5
        self.order_status_history_repository.delete_by_id(
            order_status_history_1.id, order_status_history_1
        )

        mocked_query.assert_called_with(OrderStatusHistory)

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
                OrderStatusHistory.entity_status: Status.DELETED.value,
                OrderStatusHistory.updated_date: mocked_datetime.now(),
                OrderStatusHistory.updated_by: order_status_history_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        order_status_history_1 = build_order_status_history()
        order_status_history_1.id = 5
        order_status_history_to_be_updated = build_order_status_history()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_status_history_to_be_updated)
            .get_mocked_query()
        )

        self.order_status_history_repository.update_by_id(
            order_status_history_1.id, order_status_history_1
        )

        mocked_query.assert_called_with(OrderStatusHistory)

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
        order_1 = Order()
        order_1.id = 2
        order_status_history_1 = build_order_status_history(order_id=2)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=[order_status_history_1])
            .get_mocked_query()
        )

        order_status_histories_returned = (
            self.order_status_history_repository.get_by_order_id(order_1.id)
        )
        mocked_query.assert_called_with(OrderStatusHistory)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
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
        "src.lib.repositories.impl_v2.order_status_history_repository_impl.desc"
    )
    def test_set_next_status_history_by_order_id(self, mocked_desc):
        order_1 = Order()
        order_1.id = 3

        order_status_history_to_return = build_order_status_history(order_id=order_1.id)

        query_last_order_status_history = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .order_by()
            .limit()
            .all(return_value=order_status_history_to_return)
            .get_mocked_query()
        )

        self.order_status_history_repository.set_next_status_history_by_order_id(
            order_1.id, OrderStatus.CANCELLED.name
        )

        query_last_order_status_history.assert_called_with(OrderStatusHistory)

        self.assertEqual(
            query_last_order_status_history.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            order_1.id,
        )

        self.assertEqual(
            query_last_order_status_history.return_value.filter.mock_calls[0]
            .args[0]
            .left,
            OrderStatusHistory.order_id,
        )
        self.assertEqual(
            query_last_order_status_history.return_value.filter.return_value.order_by.mock_calls[
                0
            ].args[
                0
            ],
            mocked_desc(),
        )
        self.assertEqual(
            query_last_order_status_history.return_value.filter.return_value.order_by.return_value.limit.mock_calls[
                0
            ].args[
                0
            ],
            1,
        )