import unittest
from unittest import mock

from src.constants.audit import Status
from src.lib.repositories.impl.inventory_ingredient_repository_impl import (
    InventoryIngredientRepositoryImpl,
)
from src.lib.repositories.impl.order_detail_repository_impl import (
    OrderDetailRepositoryImpl,
)
from src.lib.repositories.impl.order_repository_impl import OrderRepositoryImpl
from src.lib.repositories.impl.product_ingredient_repository_impl import (
    ProductIngredientRepositoryImpl,
)
from src.tests.utils.fixtures.inventory_ingredient_fixture import (
    build_inventory_ingredient,
)

from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.order_fixture import build_order, build_orders
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.product_ingredient_fixture import build_product_ingredient
from src.tests.utils.fixtures.product_fixture import build_product
from src.constants.order_status import OrderStatus
from src.constants.cooking_type import CookingType


class OrderRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_successfully(self):
        order = build_order()
        order_repository = OrderRepositoryImpl()

        order_repository.add(order)

        self.assertEqual(order.id, 1)

    def test_get_order_successfully(self):
        orders = build_orders(count=3)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders[0])
        order_repository.add(orders[1])
        order_repository.add(orders[2])

        found_order3 = order_repository.get_by_id(3)

        self.assertEqual(found_order3.id, 3)

    def test_get_throws_key_error_for_non_existing_order(self):
        order1 = build_order()

        order_repository = OrderRepositoryImpl()

        order_repository.add(order1)

        self.assertRaises(KeyError, order_repository.get_by_id, 2)

    def test_get_all_orders_successfully(self):
        orders_to_insert = build_orders(count=5)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])
        order_repository.add(orders_to_insert[2])
        order_repository.add(orders_to_insert[3])
        order_repository.add(orders_to_insert[4])

        orders = order_repository.get_all()

        self.assertEqual(
            orders,
            [
                orders_to_insert[0],
                orders_to_insert[1],
                orders_to_insert[2],
                orders_to_insert[3],
                orders_to_insert[4],
            ],
        )

    def test_get_all_orders_empty_successfully(self):
        order_repository = OrderRepositoryImpl()

        orders = order_repository.get_all()

        self.assertEqual(orders, [])

    def test_delete_an_order_successfully(self):
        orders_to_insert = build_orders(count=3)
        order_to_delete = build_order(entity_status=Status.DELETED)
        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])
        order_repository.add(orders_to_insert[2])

        order_repository.delete_by_id(2, order_to_delete)

        orders = order_repository.get_all()

        self.assertEqual(orders, [orders_to_insert[0], orders_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_orders(self):
        order_repository = OrderRepositoryImpl()
        order_to_delete = build_order(entity_status=Status.DELETED)
        self.assertRaises(KeyError, order_repository.delete_by_id, 2, order_to_delete)

    def test_update_order_successfully(self):
        orders_to_insert = build_orders(count=2)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])

        order_to_update = build_order(assigned_chef_id=1)

        order_repository.update_by_id(2, order_to_update)
        updated_order = order_repository.get_by_id(2)
        orders = order_repository.get_all()

        self.assertEqual(len(orders), 2)
        self.assertEqual(
            updated_order.assigned_chef_id, order_to_update.assigned_chef_id
        )

    def test_get_orders_by_status(self):
        order_1 = build_order()
        order_2 = build_order()
        order_3 = build_order(status=OrderStatus.COMPLETED)

        order_repository = OrderRepositoryImpl()
        order_repository.add(order_1)
        order_repository.add(order_2)
        order_repository.add(order_3)

        self.assertEqual(
            len(order_repository.get_orders_by_status(OrderStatus.NEW_ORDER, 10)), 2
        )

    def test_get_order_ingredients_by_order_id(self):
        product_ingredient_repository = mock.Mock(
            wraps=ProductIngredientRepositoryImpl()
        )
        order_detail_repository = mock.Mock(wraps=OrderDetailRepositoryImpl())
        ingredient_1 = build_ingredient(ingredient_id=1, name="ingredient_1")
        ingredient_2 = build_ingredient(ingredient_id=2, name="ingredient_2")
        product_1 = build_product(product_id=1, name="product_1")
        product_ingredient_1 = build_product_ingredient(
            id=1, product_id=product_1.id, ingredient_id=ingredient_1.id, quantity=2
        )
        product_ingredient_repository.add(product_ingredient_1)

        product_ingredient_2 = build_product_ingredient(
            id=2, product_id=product_1.id, ingredient_id=ingredient_2.id, quantity=2
        )
        product_ingredient_repository.add(product_ingredient_2)

        order_1 = build_order(order_id=1)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_1.id, product_id=product_1.id, quantity=1
        )
        order_detail_repository.add(order_detail_1)
        order_repository = OrderRepositoryImpl(
            order_detail_repository, product_ingredient_repository
        )
        order_ingredients = order_repository.get_order_ingredients_by_order_id(
            order_1.id
        )
        product_ingredient_repository.get_product_ingredients_by_product_ids.assert_called_with(
            [product_1.id]
        )
        order_detail_repository.get_by_order_id.assert_called_with(order_1.id)

        self.assertEqual(
            order_ingredients, [product_ingredient_1, product_ingredient_2]
        )

    def test_get_validated_orders_map(self):

        product_ingredient_repository = mock.Mock(
            wraps=ProductIngredientRepositoryImpl()
        )
        ingredient_1 = build_ingredient(ingredient_id=1, name="test_ingredient")
        inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1,
            ingredient_id=ingredient_1.id,
            ingredient_quantity=20,
        )
        product_1 = build_product(product_id=1)
        product_ingredient_1 = build_product_ingredient(
            id=1, ingredient_id=ingredient_1.id, product_id=product_1.id, quantity=2
        )
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        order_detail_1 = build_order_detail(
            order_detail_id=1, order_id=order_1.id, product_id=product_1.id, quantity=1
        )
        order_detail_repository = mock.Mock(wraps=OrderDetailRepositoryImpl())
        order_detail_repository.add(order_detail_1)
        product_ingredient_repository.add(product_ingredient_1)
        inventory_ingredient_repository = mock.Mock(
            wraps=InventoryIngredientRepositoryImpl(product_ingredient_repository)
        )
        inventory_ingredient_repository.add(inventory_ingredient_1)

        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)

        order_repository = OrderRepositoryImpl(
            inventory_ingredient_repository=inventory_ingredient_repository,
            order_detail_repository=order_detail_repository,
        )
        order_repository.add(order_1)
        order_1.order_detail_id = order_detail_1.id
        order_repository.update_by_id(order_1.id, order_1)

        orders_to_process = order_repository.get_orders_by_status(
            OrderStatus.NEW_ORDER, 10
        )
        order_validation_map = order_repository.get_validated_orders_map(
            orders_to_process
        )
        self.assertTrue(order_validation_map[order_1.id])
        order_detail_repository.get_by_order_id.assert_called_with(order_1.id)
        inventory_ingredient_repository.get_final_product_qty_by_product_ids.assert_called_with(
            [product_1.id]
        )

    def test_reduce_order_ingredients_from_inventory_successfully(self):
        ingredient_1 = build_ingredient(ingredient_id=1, name="potato")
        inventory_ingredient_1 = build_inventory_ingredient(
            inventory_ingredient_id=1,
            ingredient_id=ingredient_1.id,
            ingredient_quantity=20,
        )
        mocked_inventory_ingredient_repository = mock.Mock(
            wraps=InventoryIngredientRepositoryImpl()
        )
        mocked_inventory_ingredient_repository.add(inventory_ingredient_1)

        order_1 = build_order(order_id=1)
        product_1 = build_product(product_id=1, name="fries potatoes")
        ingredient_1 = build_ingredient(ingredient_id=1, name="potatoes")
        product_ingredient_1 = build_product_ingredient(
            id=1,
            product_id=product_1.id,
            ingredient_id=ingredient_1.id,
            ingredient_type=CookingType.FRYING,
            quantity=10,
        )
        order_detail_1 = build_order_detail(
            product_id=product_1.id, order_id=order_1.id
        )

        order_detail_repository = OrderDetailRepositoryImpl()
        order_detail_repository.add(order_detail_1)
        product_ingredient_repository = ProductIngredientRepositoryImpl()
        product_ingredient_repository.add(product_ingredient_1)
        order_repository = OrderRepositoryImpl(
            order_detail_repository=order_detail_repository,
            product_ingredient_repository=product_ingredient_repository,
            inventory_ingredient_repository=mocked_inventory_ingredient_repository,
        )
        order_repository.add(order_1)
        order_repository.reduce_order_ingredients_from_inventory(order_1.id)
        mocked_inventory_ingredient_repository.get_by_ingredient_id.assert_called_with(
            ingredient_1.id
        )
        inventory_ingredient_after_reduce = (
            mocked_inventory_ingredient_repository.get_by_id(inventory_ingredient_1.id)
        )
        self.assertEqual(inventory_ingredient_after_reduce.ingredient_quantity, 10)
