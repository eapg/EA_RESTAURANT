import unittest
from unittest import mock

from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.lib.repositories.impl.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl,
)
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.order_status_history_fixture import (
    build_order_status_histories,
    build_order_status_history,
)


class OrderStatusHistoryRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.order_status_history_repository = mock.Mock(
            wraps=OrderStatusHistoryRepositoryImpl()
        )
        self.order_status_history_controller = OrderStatusHistoryController(
            self.order_status_history_repository
        )

    def test_add_order_status_history_to_repository_using_controller(self):
        order_status_history = build_order_status_history()

        self.assertIsNone(order_status_history.id)

        self.order_status_history_controller.add(order_status_history)
        self.order_status_history_repository.add.assert_called_with(
            order_status_history
        )

    def test_get_order_status_history_from_repository_using_controller(self):
        order_status_histories = build_order_status_histories(count=3)

        self.order_status_history_controller.add(order_status_histories[0])
        self.order_status_history_controller.add(order_status_histories[1])
        self.order_status_history_controller.add(order_status_histories[2])

        found_order_status_history3 = self.order_status_history_controller.get_by_id(3)

        self.order_status_history_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_order_status_history3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_status_history(self):
        order_status_history1 = build_order_status_history()

        self.order_status_history_controller.add(order_status_history1)

        self.assertRaises(KeyError, self.order_status_history_controller.get_by_id, 2)
        self.order_status_history_repository.get_by_id.assert_called_with(2)

    def test_get_all_order_status_histories_from_repository_using_controller(self):

        order_status_histories_to_insert = build_order_status_histories(count=4)

        self.order_status_history_controller.add(order_status_histories_to_insert[0])
        self.order_status_history_controller.add(order_status_histories_to_insert[1])
        self.order_status_history_controller.add(order_status_histories_to_insert[2])
        self.order_status_history_controller.add(order_status_histories_to_insert[3])

        order_status_histories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.get_all.assert_called_with()

        self.assertEqual(
            order_status_histories,
            [
                order_status_histories_to_insert[0],
                order_status_histories_to_insert[1],
                order_status_histories_to_insert[2],
                order_status_histories_to_insert[3],
            ],
        )

    def test_get_all_order_status_histories_empty_from_repository_through_controller(
        self,
    ):
        order_status_histories = self.order_status_history_controller.get_all()
        self.order_status_history_repository.get_all.assert_called_with()
        self.assertEqual(order_status_histories, [])

    def test_delete_an_order_status_history_from_repository_using_controller(self):
        order_status_histories_to_insert = build_order_status_histories(count=4)

        self.order_status_history_controller.add(order_status_histories_to_insert[0])
        self.order_status_history_controller.add(order_status_histories_to_insert[1])
        self.order_status_history_controller.add(order_status_histories_to_insert[2])
        self.order_status_history_controller.add(order_status_histories_to_insert[3])

        self.order_status_history_controller.delete_by_id(3)
        order_status_histories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.delete_by_id.assert_called_once_with(3)

        self.assertEqual(
            order_status_histories,
            [
                order_status_histories_to_insert[0],
                order_status_histories_to_insert[1],
                order_status_histories_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_order_status_histories(self):
        self.assertRaises(
            KeyError, self.order_status_history_controller.delete_by_id, 3
        )
        self.order_status_history_repository.delete_by_id.assert_called_with(3)

    def test_update_order_status_history_from_repository_using_controller(self):
        order_status_histories_to_insert = build_order_status_histories(count=2)

        self.order_status_history_controller.add(order_status_histories_to_insert[0])
        self.order_status_history_controller.add(order_status_histories_to_insert[1])

        order_status_history_to_update = build_order_status_history(
            order=build_order(order_id=10)
        )

        self.order_status_history_controller.update_by_id(
            2, order_status_history_to_update
        )
        updated_order_status_history = self.order_status_history_controller.get_by_id(2)
        order_status_histories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.update_by_id.assert_called_once_with(
            2, order_status_history_to_update
        )

        self.assertEqual(len(order_status_histories), 2)
        self.assertEqual(
            updated_order_status_history.order, order_status_history_to_update.order
        )

    def test_get_by_order_id_from_repository_using_controller(self):
        order_1 = build_order(order_id=1)
        order_status_history_1 = build_order_status_history(order=order_1)
        order_status_history_2 = build_order_status_history()
        self.order_status_history_controller.add(order_status_history_1)
        self.order_status_history_controller.add(order_status_history_2)

        order_status_histories_returned = (
            self.order_status_history_controller.get_by_order_id(order_1.id)
        )
        self.order_status_history_repository.get_by_order_id.assert_called_with(
            order_1.id
        )
