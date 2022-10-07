import unittest
from unittest import mock

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.repositories.impl.order_status_history_repository_impl import \
    OrderStatusHistoryRepositoryImpl
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.order_status_history_fixture import (
    build_order_status_histories, build_order_status_history)


class OrderStatusHistoryRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_status_history_successfully(self):
        order_status_history = build_order_status_history()
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_history)

        self.assertEqual(order_status_history.id, 1)

    def test_get_order_status_history_successfully(self):
        order_status_histories = build_order_status_histories(count=3)

        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_histories[0])
        order_status_history_repository.add(order_status_histories[1])
        order_status_history_repository.add(order_status_histories[2])

        found_order_status_history3 = order_status_history_repository.get_by_id(3)

        self.assertEqual(found_order_status_history3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_status_history(self):
        order_status_history1 = build_order_status_history()

        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_history1)

        self.assertRaises(KeyError, order_status_history_repository.get_by_id, 2)

    def test_get_all_order_status_histories_successfully(self):
        order_status_histories_to_insert = build_order_status_histories(count=5)

        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_histories_to_insert[0])
        order_status_history_repository.add(order_status_histories_to_insert[1])
        order_status_history_repository.add(order_status_histories_to_insert[2])
        order_status_history_repository.add(order_status_histories_to_insert[3])
        order_status_history_repository.add(order_status_histories_to_insert[4])

        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(
            order_status_histories,
            [
                order_status_histories_to_insert[0],
                order_status_histories_to_insert[1],
                order_status_histories_to_insert[2],
                order_status_histories_to_insert[3],
                order_status_histories_to_insert[4],
            ],
        )

    def test_get_all_order_status_histories_empty_successfully(self):
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(order_status_histories, [])

    def test_delete_an_order_status_history_successfully(self):
        order_status_histories_to_insert = build_order_status_histories(count=3)
        order_status_history_to_delete = build_order_status_history(
            entity_status=Status.DELETED
        )
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_histories_to_insert[0])
        order_status_history_repository.add(order_status_histories_to_insert[1])
        order_status_history_repository.add(order_status_histories_to_insert[2])

        order_status_history_repository.delete_by_id(2, order_status_history_to_delete)

        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(
            order_status_histories,
            [order_status_histories_to_insert[0], order_status_histories_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_order_status_histories(self):
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()
        order_status_history_to_delete = build_order_status_history(
            entity_status=Status.DELETED
        )
        self.assertRaises(
            KeyError,
            order_status_history_repository.delete_by_id,
            2,
            order_status_history_to_delete,
        )

    def test_update_order_status_history_successfully(self):
        order_status_histories_to_insert = build_order_status_histories(count=2)

        order_status_history_repository = OrderStatusHistoryRepositoryImpl()

        order_status_history_repository.add(order_status_histories_to_insert[0])
        order_status_history_repository.add(order_status_histories_to_insert[1])

        order_status_history_to_update = build_order_status_history(order_id=5)

        order_status_history_repository.update_by_id(2, order_status_history_to_update)
        updated_order_status_history = order_status_history_repository.get_by_id(2)
        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(len(order_status_histories), 2)
        self.assertEqual(
            updated_order_status_history.order_id,
            order_status_history_to_update.order_id,
        )

    def test_get_by_order_id_successfully(self):
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()
        order_1 = build_order(order_id=1)
        order_status_history_1 = build_order_status_history(order_id=order_1.id)
        order_status_history_2 = build_order_status_history()
        order_status_history_repository.add(order_status_history_1)
        order_status_history_repository.add(order_status_history_2)

        order_status_histories_returned = (
            order_status_history_repository.get_by_order_id(order_1.id)
        )
        self.assertEqual(order_status_histories_returned[0], order_status_history_1)

    def test_set_next_status_history_by_order_id(self):
        order_status_history_repository = OrderStatusHistoryRepositoryImpl()
        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        order_status_history_repository.get_last_status_history_by_order_id = mock.Mock(
            wraps=order_status_history_repository.get_last_status_history_by_order_id
        )
        order_status_history_repository.set_next_status_history_by_order_id(
            order_1.id, order_1.status
        )
        order_1.status = OrderStatus.ORDER_PLACED
        order_status_history_repository.set_next_status_history_by_order_id(
            order_1.id, order_1.status
        )
        order_status_history_repository.get_last_status_history_by_order_id.assert_called_with(
            order_1.id
        )
        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(
            order_status_histories[0].to_time, order_status_histories[1].from_time
        )
        self.assertEqual(
            order_status_histories[0].to_status, order_status_histories[1].from_status
        )
