from unittest import mock

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.sqlalchemy_orm_mapping import (
    InventoryIngredient,
    Order,
    OrderDetail,
    ProductIngredient,
)
from src.lib.repositories.impl_v2.order_repository_impl import OrderRepositoryImpl
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.lib.repositories.sqlalchemy_mock_builder import QueryMock

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_order,
    build_orders,
    build_product_ingredient,
)
from src.tests.utils.test_util import (
    assert_filter_entity_status_active,
    assert_filter_id,
    assert_filter_filter_id, build_update_mock_query,
)


class OrderRepositoryImplTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.order_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.order_repository = OrderRepositoryImpl(self.mocked_sqlalchemy_engine)
        self.mocked_creation_session_path.start()

    def test_add_order_successfully(self):

        order_1 = build_order()

        self.order_repository.add(order_1)
        self.mocked_sqlalchemy_session.add.assert_called_with(order_1)

    def test_get_order_successfully(self):

        order_1 = build_order(order_id=1)

        # pylint: disable=R0801
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()
            .first(return_value=order_1)
            .get_mocked_query()
        )

        result = self.order_repository.get_by_id(order_1.id)
        assert_filter_entity_status_active(self, mocked_query)
        assert_filter_filter_id(self, mocked_query)
        self.assertEqual(result, order_1)

    def test_get_all_successfully(self):

        orders = build_orders(count=4)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter(return_value=orders)
            .get_mocked_query()
        )

        returned_orders = self.order_repository.get_all()

        mocked_query.assert_called_with(Order)
        assert_filter_entity_status_active(self, mocked_query)
        self.assertEqual(orders, returned_orders)

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.datetime")
    def test_delete_by_id_successfully(self, mocked_datetime):

        order_1 = build_order(order_id=1)

        order_1.updated_by = 1

        mocked_query = build_update_mock_query(self.mocked_sqlalchemy_session)

        self.order_repository.delete_by_id(order_1.id, order_1)

        mocked_query.assert_called_with(Order)
        assert_filter_id(self, mocked_query)

        mocked_query.return_value.filter.return_value.update.assert_called_with(
            {
                Order.entity_status: Status.DELETED.value,
                Order.updated_date: mocked_datetime.now(),
                Order.updated_by: order_1.updated_by,
            }
        )

    def test_update_by_id_successfully(self):

        order_1 = build_order(order_id=1)

        order_to_be_updated = build_order()
        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .first(return_value=order_to_be_updated)
            .get_mocked_query()
        )

        self.order_repository.update_by_id(order_1.id, order_1)

        mocked_query.assert_called_with(Order)
        assert_filter_id(self, mocked_query)

        self.mocked_sqlalchemy_session.add.assert_called_with(order_to_be_updated)

    def test_get_orders_by_status_successfully(self):

        order_1 = build_order(status=OrderStatus.IN_PROCESS.name)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .filter()  # pylint: disable=R0801
            .limit()
            .all(return_value=[order_1])
            .get_mocked_query()
        )

        orders_by_status = self.order_repository.get_orders_by_status(
            OrderStatus.IN_PROCESS.name, order_limit=2
        )

        mocked_query.assert_called_with(Order)

        assert_filter_entity_status_active(self, mocked_query)

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .left.key,
            "status",
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.filter.mock_calls[0]
            .args[0]
            .right.value,
            OrderStatus.IN_PROCESS.name,
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

        order_1 = build_order(order_id=1)

        product_ingredient_1 = build_product_ingredient(product_id=1)
        product_ingredient_2 = build_product_ingredient(product_id=2)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
            .query()
            .filter()
            .join()
            .filter(return_value=[product_ingredient_1, product_ingredient_2])
            .get_mocked_query()
        )

        order_ingredients = self.order_repository.get_order_ingredients_by_order_id(1)

        mocked_query.assert_called_with(ProductIngredient)
        assert_filter_entity_status_active(self, mocked_query)

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0].args[0],
            OrderDetail,
        )

        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0]
            .args[1]
            .left,
            ProductIngredient.product_id,
        )
        self.assertEqual(
            mocked_query.return_value.filter.return_value.join.mock_calls[0]
            .args[1]
            .right,
            OrderDetail.product_id,
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
            OrderDetail.order_id,
        )
        self.assertEqual(
            order_ingredients, [product_ingredient_1, product_ingredient_2]
        )

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.case")
    def test_get_validated_orders_map(self, mocked_case):

        order_1 = build_order(order_id=1)
        order_2 = build_order(order_id=2)

        mocked_query = (
            QueryMock(self.mocked_sqlalchemy_session)
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
        mocked_query.assert_called_with(OrderDetail.order_id, mocked_case())

        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[0], ProductIngredient
        )
        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[1].left,
            ProductIngredient.product_id,
        )
        self.assertEqual(
            mocked_query.return_value.join.mock_calls[0].args[1].right,
            OrderDetail.product_id,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0].args[0],
            InventoryIngredient,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0].args[1].left,
            ProductIngredient.ingredient_id,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.mock_calls[0]
            .args[1]
            .right,
            InventoryIngredient.ingredient_id,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .left,
            OrderDetail.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[0]
            .right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[1]
            .left,
            ProductIngredient.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[1]
            .right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[2]
            .left,
            InventoryIngredient.entity_status,
        )
        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[2]
            .right.value,
            Status.ACTIVE.value,
        )

        self.assertEqual(
            mocked_query.return_value.join.return_value.join.return_value.filter.mock_calls[
                0
            ]
            .args[3]
            .left,
            OrderDetail.order_id,
        )

        self.assertEqual(order_validation_map, {1: True, 2: True})

    @mock.patch("src.lib.repositories.impl_v2.order_repository_impl.text")
    def test_reduce_order_ingredients_from_inventory(self, mocked_text):

        order_1 = build_order(order_id=1)

        self.order_repository.reduce_order_ingredients_from_inventory(order_1.id)

        self.assertEqual(
            self.mocked_sqlalchemy_engine.mock_calls[2].args[0], mocked_text()
        )
        self.assertEqual(
            self.mocked_sqlalchemy_engine.mock_calls[2].args[1],
            {"order_id": order_1.id},
        )
