from unittest import mock

from src.constants.audit import Status
from src.lib.repositories.impl_v2.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.lib.repositories.impl_v2.order_detail_repository_impl import (
    OrderDetailRepositoryImpl,
)
from src.lib.repositories.impl_v2.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock


# building asserts:
def assert_filter_entity_status_active(self, mocked_query):
    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
        "entity_status",
    )

    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
        Status.ACTIVE.value,
    )


def assert_filter_id(self, mocked_query):
    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
        "id",
    )

    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
        1,
    )


def assert_filter_filter_id(self, mocked_query):
    self.assertEqual(
        mocked_query.return_value.filter.return_value.filter.mock_calls[0]
        .args[0]
        .left.key,
        "id",
    )

    self.assertEqual(
        mocked_query.return_value.filter.return_value.filter.mock_calls[0]
        .args[0]
        .right.value,
        1,
    )


def assert_filter_value_id(self, mocked_query, value=None):
    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
        value,
    )

    self.assertEqual(
        mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
        1,
    )


def assert_filter_filter_value_id(self, mocked_query, value=None):
    self.assertEqual(
        mocked_query.return_value.filter.return_value.filter.mock_calls[0]
        .args[0]
        .left.key,
        value,
    )

    self.assertEqual(
        mocked_query.return_value.filter.return_value.filter.mock_calls[0]
        .args[0]
        .right.value,
        1,
    )


# Building repositories patch:
def get_product_ingredient_repository_with_session_pathed(self):
    self.mocked_creation_session_path = mock.patch(
        "src.lib.repositories.impl_v2.product_ingredient_repository_impl.create_session",
        return_value=self.mocked_sqlalchemy_session,
    )
    self.product_ingredient_repository = mock.Mock(
        wraps=ProductIngredientRepositoryImpl(self.mocked_sqlalchemy_engine)
    )
    self.mocked_creation_session_path.start()
    return self.product_ingredient_repository


def get_order_detail_repository_with_session_patched(self):
    self.mocked_creation_session_path = mock.patch(
        "src.lib.repositories.impl_v2.order_detail_repository_impl.create_session",
        return_value=self.mocked_sqlalchemy_session,
    )
    self.order_detail_repository = mock.Mock(
        wraps=OrderDetailRepositoryImpl(self.mocked_sqlalchemy_engine)
    )
    self.mocked_creation_session_path.start()
    return self.order_detail_repository


def get_inventory_ingredient_repository_with_session_patched(self):
    self.mocked_creation_session_path = mock.patch(
        "src.lib.repositories.impl_v2.inventory_ingredient_repository_impl.create_session",
        return_value=self.mocked_sqlalchemy_session,
    )
    self.inventory_ingredient_repository = mock.Mock(
        wraps=InventoryIngredientRepositoryImpl(self.mocked_sqlalchemy_engine)
    )
    self.mocked_creation_session_path.start()
    return self.inventory_ingredient_repository


# building mock queries:


def build_update_mock_query(mocked_sqlalchemy_session):
    mocked_query = (
        QueryMock(mocked_sqlalchemy_session)
        .query()
        .filter()
        .update()
        .get_mocked_query()
    )
    return mocked_query
