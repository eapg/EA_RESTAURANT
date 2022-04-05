import unittest
from unittest import mock

from src.api.controllers.order_controller import OrderController
from src.lib.repositories.impl.order_repository_impl import (
    OrderRepositoryImpl,
)
from src.tests.utils.fixtures.order_fixture import (
    build_order,
    build_orders,
)
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail


class OrderRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = mock.Mock(wraps=OrderRepositoryImpl())
        self.order_controller = OrderController(self.order_repository)

    def test_add_order_to_repository_using_controller(self):
        order = build_order()

        self.assertIsNone(order.id)

        self.order_controller.add(order)
        self.order_repository.add.assert_called_with(order)

    def test_get_order_from_repository_using_controller(self):
        orders = build_orders(count=3)

        self.order_controller.add(orders[0])
        self.order_controller.add(orders[1])
        self.order_controller.add(orders[2])

        found_order3 = self.order_controller.get_by_id(3)

        self.order_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_order3.id, 3)

    def test_get_throws_key_error_for_non_existing_order(self):
        order1 = build_order()

        self.order_controller.add(order1)

        self.assertRaises(KeyError, self.order_controller.get_by_id, 2)
        self.order_repository.get_by_id.assert_called_with(2)

    def test_get_all_orders_from_repository_using_controller(self):

        orders_to_insert = build_orders(count=4)

        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])
        self.order_controller.add(orders_to_insert[2])
        self.order_controller.add(orders_to_insert[3])

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
        orders = self.order_controller.get_all()
        self.order_repository.get_all.assert_called_with()
        self.assertEqual(orders, [])

    def test_delete_an_order_from_repository_using_controller(self):
        orders_to_insert = build_orders(count=4)

        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])
        self.order_controller.add(orders_to_insert[2])
        self.order_controller.add(orders_to_insert[3])

        self.order_controller.delete_by_id(3)
        orders = self.order_controller.get_all()

        self.order_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            orders,
            [
                orders_to_insert[0],
                orders_to_insert[1],
                orders_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_orders(self):
        self.assertRaises(KeyError, self.order_controller.delete_by_id, 3)
        self.order_repository.delete_by_id.assert_called_with(3)

    def test_update_order_from_repository_using_controller(self):
        orders_to_insert = build_orders(count=2)

        self.order_controller.add(orders_to_insert[0])
        self.order_controller.add(orders_to_insert[1])

        order_to_update = build_order(order_details=build_order_detail())

        self.order_controller.update_by_id(2, order_to_update)
        updated_order = self.order_controller.get_by_id(2)
        orders = self.order_controller.get_all()

        self.order_repository.update_by_id.assert_called_once_with(2, order_to_update)

        self.assertEqual(len(orders), 2)
        self.assertEqual(updated_order.order_details, order_to_update.order_details)
