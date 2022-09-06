from unittest import mock

from src.constants import audit, order_status
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.impl_v2 import order_repository_impl
from src.tests.lib.repositories import (
    sqlalchemy_base_repository_impl_test,
    sqlalchemy_mock_builder,
)
from src.tests.utils.fixtures import mapping_orm_fixtures


class OrderRepositoryImplTestCase(
    sqlalchemy_base_repository_impl_test.SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.order_repository = order_repository_impl.OrderRepositoryImpl()

    def test_add_order_successfully(self):
        order_1 = mapping_orm_fixtures.build_order()

        self.order_repository.add(order_1)
        self.order_repository.session.add.assert_called_with(order_1)

    def test_get_order_successfully(self):
        order_1 = mapping_orm_fixtures.build_order()

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=order_1)
            .get_mocked_query()
        )
        order_1.id = 5
        result = self.order_repository.get_by_id(order_1.id)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Order)
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key, "id"
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_1.id,
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
        self.assertEqual(result, order_1)

    def test_get_all_successfully(self):
        orders = mapping_orm_fixtures.build_orders(count=4)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=orders)
            .get_mocked_query()
        )

        returned_orders = self.order_repository.get_all()

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Order)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )
        self.assertEqual(orders, returned_orders)

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.datetime")
    def test_delete_by_id_successfully(self, mocked_datetime):
        order_1 = mapping_orm_fixtures.build_order()

        order_1.updated_by = 1

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .update()
            .get_mocked_query()
        )

        order_1.id = 5
        self.order_repository.delete_by_id(order_1.id, order_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Order)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_1.id,
        )

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                sqlalchemy_orm_mapping.Order.entity_status: audit.Status.DELETED.value,
                sqlalchemy_orm_mapping.Order.updated_date: mocked_datetime.now(),
                sqlalchemy_orm_mapping.Order.updated_by: order_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):
        order_1 = mapping_orm_fixtures.build_order()

        order_1.id = 5
        order_to_be_updated = mapping_orm_fixtures.build_order()
        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_to_be_updated)
            .get_mocked_query()
        )

        self.order_repository.update_by_id(order_1.id, order_1)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Order)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "id",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            order_1.id,
        )

        self.order_repository.session.add.assert_called_with(order_to_be_updated)

    def test_get_orders_by_status_successfully(self):

        order_1 = mapping_orm_fixtures.build_order(
            status=order_status.OrderStatus.IN_PROCESS.name
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .limit()
            .all(return_value=[order_1])
            .get_mocked_query()
        )

        orders_by_status = self.order_repository.get_orders_by_status(
            order_status.OrderStatus.IN_PROCESS.name, order_limit=2
        )

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.Order)

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
            "status",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.return_value.limit.mock_calls[
                0
            ].args[
                0
            ],
            2,
        )
        self.assertEqual(orders_by_status, [order_1])

    def test_get_order_ingredients_by_order_id(self):

        order_1 = mapping_orm_fixtures.build_order()
        order_1.id = 5

        product_ingredient_1 = mapping_orm_fixtures.build_product_ingredient(
            product_id=1
        )
        product_ingredient_2 = mapping_orm_fixtures.build_product_ingredient(
            product_id=2
        )

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .join()
            .filter(return_value=[product_ingredient_1, product_ingredient_2])
            .get_mocked_query()
        )

        order_ingredients = self.order_repository.get_order_ingredients_by_order_id(5)

        mocked_query.assert_called_with(sqlalchemy_orm_mapping.ProductIngredient)

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[0].right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[1].left.key,
            "entity_status",
        )
        self.assertEqual(
            mocked_query.return_value.filter.mock_calls[0].args[1].right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0].args[0],
            sqlalchemy_orm_mapping.OrderDetail,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0]
            .args[1]
            .left,
            sqlalchemy_orm_mapping.ProductIngredient.product_id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0]
            .args[1]
            .right,
            sqlalchemy_orm_mapping.OrderDetail.product_id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            order_1.id,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left,
            sqlalchemy_orm_mapping.OrderDetail.order_id,
        )
        self.assertEqual(
            order_ingredients, [product_ingredient_1, product_ingredient_2]
        )

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.sqlalchemy.case")
    def test_get_validated_orders_map(self, mocked_case):
        order_1 = mapping_orm_fixtures.build_order(order_id=1)
        order_2 = mapping_orm_fixtures.build_order(order_id=2)

        mocked_query = (
            sqlalchemy_mock_builder.QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .join()
            .join()
            .filter()
            .group_by()
            .all(return_value=[(1, True), (2, True)])
            .get_mocked_query()
        )

        order_validation_map = self.order_repository.get_validated_orders_map(
            [order_1, order_2]
        )
        mocked_query.assert_called_with(
            sqlalchemy_orm_mapping.OrderDetail.order_id, mocked_case()
        )

        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[0],
            sqlalchemy_orm_mapping.ProductIngredient,
        )
        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[1].left,
            sqlalchemy_orm_mapping.ProductIngredient.product_id,
        )
        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[1].right,
            sqlalchemy_orm_mapping.OrderDetail.product_id,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0].args[0],
            sqlalchemy_orm_mapping.InventoryIngredient,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0].args[1].left,
            sqlalchemy_orm_mapping.ProductIngredient.ingredient_id,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0]
            .args[1]
            .right,
            sqlalchemy_orm_mapping.InventoryIngredient.ingredient_id,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left,
            sqlalchemy_orm_mapping.OrderDetail.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[1]
            .left,
            sqlalchemy_orm_mapping.ProductIngredient.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[1]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[2]
            .left,
            sqlalchemy_orm_mapping.InventoryIngredient.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[2]
            .right.value,
            audit.Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[3]
            .left,
            sqlalchemy_orm_mapping.OrderDetail.order_id,
        )

        self.assertEqual(order_validation_map, {1: True, 2: True})

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.sql.text")
    def test_reduce_order_ingredients_from_inventory(self, mocked_text):
        order_1 = mapping_orm_fixtures.build_order()
        order_1.id = 5

        self.order_repository.reduce_order_ingredients_from_inventory(order_1.id)

        self.assertEqual(
            self.mocked_sqlalchemy_session.mock_calls[3].args[0], mocked_text()
        )
        self.assertEqual(
            self.mocked_sqlalchemy_session.mock_calls[3].args[1],
            {"order_id": order_1.id},
        )
