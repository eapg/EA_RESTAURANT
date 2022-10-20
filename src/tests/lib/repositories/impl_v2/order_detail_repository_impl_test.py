from unittest import mock

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import OrderDetail
from src.lib.repositories.impl_v2.order_detail_repository_impl import (
    OrderDetailRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_order_detail,
    build_order_details,
    build_order,
)
from src.tests.utils.test_util import (
    assert_filter_id,
    assert_filter_filter_id,
    assert_filter_entity_status_active,
    assert_filter_filter_value_id, build_update_mock_query,
)


class OrderDetailRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.order_detail_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.order_detail_repository = OrderDetailRepositoryImpl(
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

    def test_add_order_detail_successfully(self):

        order_detail_1 = build_order_detail()

        self.order_detail_repository.add(order_detail_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(order_detail_1)

    def test_get_order_detail_successfully(self):

        order_detail_1 = build_order_detail(order_detail_id=1)

        # pylint: disable=R0801
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=order_detail_1)
            .get_mocked_query()
        )

        result = self.order_detail_repository.get_by_id(order_detail_1.id)

        mocked_query.assert_called_with(OrderDetail)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_id(self, mocked_query)
        self.assertEqual(result, order_detail_1)

    def test_get_all_order_details_successfully(self):

        order_details = build_order_details(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=order_details)
            .get_mocked_query()
        )

        returned_order_details = self.order_detail_repository.get_all()

        mocked_query.assert_called_with(OrderDetail)
        assert_filter_entity_status_active(self, mocked_query)

        self.assertEqual(order_details, returned_order_details)

    @mock.patch("src.lib.repositories.impl_v2.order_detail_repository_impl.datetime")
    def test_delete_an_order_detail_successfully(self, mocked_datetime):

        order_detail_1 = build_order_detail(order_detail_id=1)
        order_detail_1.updated_by = 1

        mocked_query = build_update_mock_query(self.mocked_sqlalchemy_session)

        self.order_detail_repository.delete_by_id(order_detail_1.id, order_detail_1)

        mocked_query.assert_called_with(OrderDetail)
        assert_filter_id(self, mocked_query)

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                OrderDetail.entity_status: Status.DELETED.value,
                OrderDetail.updated_date: mocked_datetime.now(),
                OrderDetail.updated_by: order_detail_1.updated_by,
            }
        )

    def test_update_order_detail_successfully(self):

        order_detail_1 = build_order_detail(order_detail_id=1)

        order_detail_to_be_updated = build_order_detail()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_detail_to_be_updated)
            .get_mocked_query()
        )

        self.order_detail_repository.update_by_id(order_detail_1.id, order_detail_1)

        mocked_query.assert_called_with(OrderDetail)
        assert_filter_id(self, mocked_query)

        self.mocked_sqlalchemy_session.add.assert_called_with(
            order_detail_to_be_updated
        )

    def test_get_by_order_id_successfully(self):

        order_1 = build_order(order_id=1)
        order_detail_1 = build_order_detail(order_id=order_1.id)
        order_detail_2 = build_order_detail(order_id=order_1.id)

        order_details_of_order_1 = [order_detail_1, order_detail_2]

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter(return_value=order_details_of_order_1)
            .get_mocked_query()
        )

        order_details_returned = self.order_detail_repository.get_by_order_id(
            order_1.id
        )

        mocked_query.assert_called_with(OrderDetail)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_value_id(self, mocked_query, value="order_id")
        self.assertEqual(order_details_returned, order_details_of_order_1)
