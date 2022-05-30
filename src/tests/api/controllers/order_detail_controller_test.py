import unittest
from unittest import mock

from src.api.controllers.order_detail_controller import (
    OrderDetailController,
)
from src.tests.utils.fixtures.order_detail_fixture import (
    build_order_detail,
    build_order_details,
)


class OrderDetailRepositoryControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.order_detail_repository = mock.Mock()
        self.order_detail_controller = OrderDetailController(
            self.order_detail_repository
        )

    def test_add_order_detail_successfully(self):
        order_detail = build_order_detail()

        self.order_detail_controller.add(order_detail)

        self.order_detail_repository.add.assert_called_with(order_detail)

    def test_get_order_detail_successfully(self):
        order_detail = build_order_detail()

        self.order_detail_repository.get_by_id.return_value = order_detail

        expected_order_detail = self.order_detail_controller.get_by_id(order_detail.id)

        self.order_detail_repository.get_by_id.assert_called_with(order_detail.id)
        self.assertEqual(expected_order_detail.id, order_detail.id)

    def test_get_all_order_details_successfully(self):
        order_details = build_order_details(count=3)

        self.order_detail_repository.get_all.return_value = order_details

        expected_order_details = self.order_detail_controller.get_all()

        self.order_detail_repository.get_all.assert_called()
        self.assertEqual(expected_order_details, order_details)
        self.assertEqual(len(expected_order_details), 3)

    def test_delete_an_order_detail_successfully(self):
        self.order_detail_controller.delete_by_id(2)

        self.order_detail_repository.delete_by_id.assert_called_with(2)

    def test_update_an_order_detail_successfully(self):
        order_detail = build_order_detail()

        self.order_detail_controller.update_by_id(1, order_detail)

        self.order_detail_repository.update_by_id.assert_called_with(1, order_detail)

    def test_get_by_order_id_successfully(self):
        order_detail_1 = build_order_detail(order_id=1)
        order_detail_2 = build_order_detail(order_id=1)

        self.order_detail_repository.get_by_order_id.return_value = [
            order_detail_1,
            order_detail_2,
        ]
        expected_order_details = self.order_detail_controller.get_by_order_id(
            order_detail_1.order_id
        )
        self.order_detail_repository.get_by_order_id.assert_called_with(
            order_detail_1.order_id
        )
        self.assertEqual(expected_order_details, [order_detail_1, order_detail_2])
