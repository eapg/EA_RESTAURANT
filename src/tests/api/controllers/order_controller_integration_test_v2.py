from unittest import mock

from src.api.controllers.order_controller import OrderController
from src.constants.audit import Status
from src.constants.order_status import OrderStatus

from src.lib.repositories.impl_v2.order_repository_impl import OrderRepositoryImpl

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_ingredient,
    build_order,
    build_orders,
    build_product,
    build_product_ingredient,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)


class OrderRepositoryControllerIntegrationTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):

        self.order_repository = mock.Mock(
            wraps=OrderRepositoryImpl(self.mocked_sqlalchemy_session)
        )
        self.order_controller = OrderController(self.order_repository)

    def test_add_order_to_repository_using_controller(self):
        order = build_order()

        self.order_controller.add(order)
        self.order_repository.add.assert_called_with(order)

    def test_get_order_from_repository_using_controller(self):
        orders = build_orders(count=3)

        self.order_controller.add(orders[0])
        self.order_controller.add(orders[1])
        self.order_controller.add(orders[2])
        self.order_repository.get_by_id.return_value = orders[2]
        found_order2 = self.order_controller.get_by_id(2)

        self.order_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_order2.id, 2)

    def test_get_all_orders_from_repository_using_controller(self):

        orders_to_insert = build_orders(count=4)

        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])
        self.order_controller.add(orders_to_insert[2])
        self.order_controller.add(orders_to_insert[3])

        self.order_repository.get_all.return_value = orders_to_insert
        orders = self.order_controller.get_all()

        self.order_repository.get_all.assert_called_with()

        self.assertEqual(
            orders,
            [
                orders_to_insert[0],
                orders_to_insert[1],
                orders_to_insert[2],
                orders_to_insert[3],
            ],
        )

    def test_get_all_orders_empty_from_repository_through_controller(self):
        self.order_repository.get_all.return_value = []
        orders = self.order_controller.get_all()
        self.order_repository.get_all.assert_called_with()
        self.assertEqual(orders, [])

    def test_delete_an_order_from_repository_using_controller(self):
        orders_to_insert = build_orders(count=4)
        order_to_delete = build_order(entity_status=Status.DELETED)
        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])
        self.order_controller.add(orders_to_insert[2])
        self.order_controller.add(orders_to_insert[3])

        self.order_controller.delete_by_id(3, order_to_delete)
        self.order_repository.get_all.return_value = [
            orders_to_insert[0],
            orders_to_insert[1],
            orders_to_insert[3],
        ]
        orders = self.order_controller.get_all()

        self.order_repository.delete_by_id.assert_called_once_with(3, order_to_delete)

        self.assertEqual(
            orders,
            [
                orders_to_insert[0],
                orders_to_insert[1],
                orders_to_insert[3],
            ],
        )

    def test_update_order_from_repository_using_controller(self):
        orders_to_insert = build_orders(count=2)

        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])

        order_to_update = build_order(assigned_chef_id=2)

        self.order_controller.update_by_id(2, order_to_update)
        self.order_repository.get_by_id.return_value = order_to_update
        updated_order = self.order_controller.get_by_id(2)
        self.order_repository.get_all.return_value = orders_to_insert
        orders = self.order_controller.get_all()

        self.order_repository.update_by_id.assert_called_once_with(2, order_to_update)

        self.assertEqual(len(orders), 2)
        self.assertEqual(
            updated_order.assigned_chef_id, order_to_update.assigned_chef_id
        )

    def test_get_orders_by_status_successfully(self):

        order_1 = build_order()
        order_2 = build_order()
        order_3 = build_order(status=OrderStatus.COMPLETED)

        self.order_controller.add(order_1)
        self.order_controller.add(order_2)
        self.order_controller.add(order_3)
        self.order_repository.get_orders_by_status.return_value = [order_1, order_2]
        orders_by_status = self.order_controller.get_orders_by_status(
            OrderStatus.NEW_ORDER, 10
        )
        self.order_repository.get_orders_by_status.assert_called_with(
            OrderStatus.NEW_ORDER, 10
        )
        self.assertEqual(orders_by_status, [order_1, order_2])

    def test_get_order_ingredients_by_order_id_from_repository_using_controller(self):

        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")
        ingredient_2 = build_ingredient(ingredient_id=2, name="ingredient_2")
        product_1 = build_product(product_id=1, name="product_1")
        product_ingredient_1 = build_product_ingredient(
            product_ingredient_id=1,
            product_id=product_1.id,
            ingredient_id=ingredient_1.id,
            quantity=2,
        )

        product_ingredient_2 = build_product_ingredient(
            product_ingredient_id=2,
            product_id=product_1.id,
            ingredient_id=ingredient_2.id,
            quantity=2,
        )

        order_1 = build_order(order_id=1)

        self.order_repository.get_order_ingredients_by_order_id.return_value = [
            product_ingredient_1,
            product_ingredient_2,
        ]
        order_ingredients = self.order_controller.get_order_ingredients_by_order_id(
            order_1.id
        )
        self.order_repository.get_order_ingredients_by_order_id.assert_called_with(
            order_1.id
        )

        self.assertEqual(
            order_ingredients, [product_ingredient_1, product_ingredient_2]
        )

    def test_get_validated_orders_map_from_repository_using_controller(self):

        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)

        self.order_controller.add(order_1)
        self.order_repository.get_orders_by_status.return_value = order_1
        orders_to_process = self.order_controller.get_orders_by_status(
            OrderStatus.NEW_ORDER, 10
        )
        self.order_repository.get_validated_orders_map.return_value = {order_1.id: True}
        order_validation_map = self.order_controller.get_validated_orders_map(
            orders_to_process
        )
        self.assertTrue(order_validation_map[order_1.id])

    def test_reduce_order_ingredients_from_inventory_from_repository_using_controller(
        self,
    ):

        order_1 = build_order(order_id=1)

        self.order_controller.add(order_1)
        self.order_controller.reduce_order_ingredients_from_inventory(order_1.id)
        self.order_repository.reduce_order_ingredients_from_inventory.assert_called_with(
            order_1.id
        )
