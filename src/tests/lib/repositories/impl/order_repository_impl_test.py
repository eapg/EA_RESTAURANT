import unittest

from src.lib.repositories.impl.order_repository_impl import OrderRepositoryImpl
from src.tests.utils.fixtures.order_fixture import build_order, build_orders
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail


class OrderRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_successfully(self):
        order = build_order()
        order_repository = OrderRepositoryImpl()

        self.assertIsNone(order.id)

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

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])
        order_repository.add(orders_to_insert[2])

        order_repository.delete_by_id(2)

        orders = order_repository.get_all()

        self.assertEqual(orders, [orders_to_insert[0], orders_to_insert[2]])

    def test_delete_throws_key_error_when_there_are_no_orders(self):
        order_repository = OrderRepositoryImpl()

        self.assertRaises(KeyError, order_repository.delete_by_id, 2)

    def test_update_order_successfully(self):
        orders_to_insert = build_orders(count=2)

        order_repository = OrderRepositoryImpl()

        order_repository.add(orders_to_insert[0])
        order_repository.add(orders_to_insert[1])

        order_to_update = build_order(order_details=build_order_detail())

        order_repository.update_by_id(2, order_to_update)
        updated_order = order_repository.get_by_id(2)
        orders = order_repository.get_all()

        self.assertEqual(len(orders), 2)
        self.assertEqual(updated_order.order_details, order_to_update.order_details)
