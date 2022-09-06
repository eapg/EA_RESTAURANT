from unittest import mock

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.sqlalchemy_orm_mapping import Chef, Order
from src.lib.repositories.impl_v2.chef_repository_impl import ChefRepositoryImpl
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import build_chef, build_chefs
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock


class ChefRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.chef_repository = ChefRepositoryImpl(self.mocked_sqlalchemy_session)

    def test_add_chef_successfully(self):
        chef_1 = build_chef(entity_status="ACTIVE", skill=2, create_by=1, user_id=1)

        self.chef_repository.add(chef_1)
        self.chef_repository.session.add.assert_called_with(chef_1)

    def test_get_chef_successfully(self):
        chef_1 = build_chef(entity_status="ACTIVE", skill=2, create_by=1, user_id=1)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=chef_1)
            .get_mocked_query()
        )
        chef_1.id = 5
        result = self.chef_repository.get_by_id(chef_1.id)

        mocked_query.assert_called_with(Chef)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            chef_1.id,
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
        self.assertEqual(result, chef_1)

    def test_get_all_chefs_successfully(self):
        chefs = build_chefs(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=chefs)
            .get_mocked_query()
        )

        returned_chefs = self.chef_repository.get_all()

        mocked_query.assert_called_with(Chef)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(chefs, returned_chefs)

    @mock.patch("src.lib.repositories.impl_v2.chef_repository_impl.datetime")
    def test_delete_an_chef_successfully(self, mocked_datetime):
        chef_1 = build_chef(entity_status="ACTIVE", skill=2, create_by=1, user_id=1)
        chef_1.updated_by = 1

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        chef_1.id = 5
        self.chef_repository.delete_by_id(chef_1.id, chef_1)

        mocked_query.assert_called_with(Chef)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            chef_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                Chef.entity_status: Status.DELETED.value,
                Chef.updated_date: mocked_datetime.now(),
                Chef.updated_by: chef_1.updated_by,
            }
        )

    def test_update_chef_successfully(self):
        chef_1 = build_chef(entity_status="ACTIVE", skill=2, create_by=1, user_id=1)
        chef_1.id = 5
        chef_to_be_updated = build_chef()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=chef_to_be_updated)
            .get_mocked_query()
        )

        self.chef_repository.update_by_id(chef_1.id, chef_1)

        mocked_query.assert_called_with(Chef)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            chef_1.id,
        )

        self.chef_repository.session.add.assert_called_with(chef_to_be_updated)

    def test_get_available_chefs(self):

        chef_1 = build_chef(chef_id=1)
        chef_2 = build_chef(chef_id=2)
        chef_3 = build_chef(chef_id=3)
        available_chef_ids = [(chef_1.id,), (chef_2.id,), (chef_3.id,)]

        mocked_chefs_query = (
            QueryMock()
            .query()
            .filter()
            .filter(return_value=available_chef_ids)
            .get_mocked_query()
        )

        mocked_orders_query = (
            QueryMock().query().filter().filter().filter().exists().get_mocked_query()
        )

        def mock_query_side_effect(t):
            return (
                mocked_chefs_query.return_value
                if t == Chef.id
                else mocked_orders_query.return_value
            )

        QueryMock(self.mocked_sqlalchemy_session).query(
            side_effect_fn=mock_query_side_effect
        )

        result = self.chef_repository.get_available_chefs()

        self.assertEqual(
            mocked_chefs_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_chefs_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )
        self.assertEqual(
            mocked_orders_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_orders_query.return_value.filter.mock_calls[0].args[0].right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_orders_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left,
            Order.assigned_chef_id,
        )
        self.assertEqual(
            mocked_orders_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right,
            Chef.id,
        )
        self.assertEqual(
            mocked_orders_query.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left,
            Order.status,
        )
        self.assertEqual(
            mocked_orders_query.return_value.filter.return_value.filter.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            OrderStatus.IN_PROCESS.name,
        )
        self.assertEqual(result, [chef_id[0] for chef_id in available_chef_ids])
