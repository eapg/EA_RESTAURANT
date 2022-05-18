import unittest
from unittest import mock

from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.order_status_history_fixture import (
    build_order_status_histories,
    build_order_status_history,
)


class OrderStatusHistoryRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_status_history_repository = mock.Mock()
        self.order_status_history_controller = OrderStatusHistoryController(
            self.order_status_history_repository
        )

    def test_add_order_status_history_successfully(self):
        order_status_history = build_order_status_history()

        self.order_status_history_controller.add(order_status_history)

        self.order_status_history_repository.add.assert_called_with(
            order_status_history
        )

    def test_get_order_status_history_successfully(self):
        order_status_history = build_order_status_history()

        self.order_status_history_repository.get_by_id.return_value = (
            order_status_history
        )

        expected_order_status_history = self.order_status_history_controller.get_by_id(
            order_status_history.id
        )

        self.order_status_history_repository.get_by_id.assert_called_with(
            order_status_history.id
        )
        self.assertEqual(expected_order_status_history.id, order_status_history.id)

    def test_get_all_order_status_histories_successfully(self):
        order_status_histories = build_order_status_histories(count=3)

        self.order_status_history_repository.get_all.return_value = (
            order_status_histories
        )

        expected_order_status_histories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.get_all.assert_called()
        self.assertEqual(expected_order_status_histories, order_status_histories)
        self.assertEqual(len(expected_order_status_histories), 3)

    def test_delete_an_order_status_history_successfully(self):
        self.order_status_history_controller.delete_by_id(2)

        self.order_status_history_repository.delete_by_id.assert_called_with(2)

    def test_update_an_order_status_history_successfully(self):
        order_status_history = build_order_status_history()

        self.order_status_history_controller.update_by_id(1, order_status_history)

        self.order_status_history_repository.update_by_id.assert_called_with(
            1, order_status_history
        )

    def test_get_by_order_id_successfully(self):
        order_status_history = build_order_status_history()
        order_1 = build_order()
        self.order_status_history_controller.add(order_status_history)
        order_status_histories_returned = (
            self.order_status_history_controller.get_by_order_id(order_1.id)
        )
        self.order_status_history_repository.get_by_order_id.assert_called_with(
            order_1.id
        )
