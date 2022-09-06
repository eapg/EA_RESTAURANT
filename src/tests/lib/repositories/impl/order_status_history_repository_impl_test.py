import unittest
from unittest import mock

from src.constants import audit
from src.constants import order_status
from src.lib.repositories.impl import order_status_history_repository_impl
from src.tests.utils.fixtures import order_fixture
from src.tests.utils.fixtures import order_status_history_fixture


class OrderStatusHistoryRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_status_history_successfully(self):
        order_status_history = order_status_history_fixture.build_order_status_history()
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

        order_status_history_repository.add(order_status_history)

        self.assertEqual(order_status_history.id, 1)

    def test_get_order_status_history_successfully(self):
        order_status_histories = (
            order_status_history_fixture.build_order_status_histories(count=3)
        )

        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

        order_status_history_repository.add(order_status_histories[0])
        order_status_history_repository.add(order_status_histories[1])
        order_status_history_repository.add(order_status_histories[2])

        found_order_status_history3 = order_status_history_repository.get_by_id(3)

        self.assertEqual(found_order_status_history3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_status_history(self):
        order_status_history1 = (
            order_status_history_fixture.build_order_status_history()
        )

        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

        order_status_history_repository.add(order_status_history1)

        self.assertRaises(KeyError, order_status_history_repository.get_by_id, 2)

    def test_get_all_order_status_histories_successfully(self):
        order_status_histories_to_insert = (
            order_status_history_fixture.build_order_status_histories(count=5)
        )

        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

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
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(order_status_histories, [])

    def test_delete_an_order_status_history_successfully(self):
        order_status_histories_to_insert = (
            order_status_history_fixture.build_order_status_histories(count=3)
        )
        order_status_history_to_delete = (
            order_status_history_fixture.build_order_status_history(
                entity_status=audit.Status.DELETED
            )
        )
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

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
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )
        order_status_history_to_delete = (
            order_status_history_fixture.build_order_status_history(
                entity_status=audit.Status.DELETED
            )
        )
        self.assertRaises(
            KeyError,
            order_status_history_repository.delete_by_id,
            2,
            order_status_history_to_delete,
        )

    def test_update_order_status_history_successfully(self):
        order_status_histories_to_insert = (
            order_status_history_fixture.build_order_status_histories(count=2)
        )

        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )

        order_status_history_repository.add(order_status_histories_to_insert[0])
        order_status_history_repository.add(order_status_histories_to_insert[1])

        order_status_history_to_update = (
            order_status_history_fixture.build_order_status_history(order_id=5)
        )

        order_status_history_repository.update_by_id(2, order_status_history_to_update)
        updated_order_status_history = order_status_history_repository.get_by_id(2)
        order_status_histories = order_status_history_repository.get_all()

        self.assertEqual(len(order_status_histories), 2)
        self.assertEqual(
            updated_order_status_history.order_id,
            order_status_history_to_update.order_id,
        )

    def test_get_by_order_id_successfully(self):
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )
        order_1 = order_fixture.build_order(order_id=1)
        order_status_history_1 = (
            order_status_history_fixture.build_order_status_history(order_id=order_1.id)
        )
        order_status_history_2 = (
            order_status_history_fixture.build_order_status_history()
        )
        order_status_history_repository.add(order_status_history_1)
        order_status_history_repository.add(order_status_history_2)

        order_status_histories_returned = (
            order_status_history_repository.get_by_order_id(order_1.id)
        )
        self.assertEqual(order_status_histories_returned[0], order_status_history_1)

    def test_set_next_status_history_by_order_id(self):
        order_status_history_repository = (
            order_status_history_repository_impl.OrderStatusHistoryRepositoryImpl()
        )
        order_1 = order_fixture.build_order(
            order_id=1, status=order_status.OrderStatus.NEW_ORDER
        )
        order_status_history_repository.get_last_status_history_by_order_id = mock.Mock(
            wraps=order_status_history_repository.get_last_status_history_by_order_id
        )
        order_status_history_repository.set_next_status_history_by_order_id(
            order_1.id, order_1.status
        )
        order_1.status = order_status.OrderStatus.ORDER_PLACED
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
