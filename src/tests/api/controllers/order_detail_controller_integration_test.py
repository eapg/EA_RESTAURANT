import unittest
from unittest import mock

from src.api.controllers.order_detail_controller import (
    OrderDetailController,
)
from src.constants.audit import Status
from src.lib.repositories.impl.order_detail_repository_impl import (
    OrderDetailRepositoryImpl,
)
from src.tests.utils.fixtures.order_detail_fixture import (
    build_order_detail,
    build_order_details,
)
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.product_fixture import build_product


class OrderDetailRepositoryControllerIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.order_detail_repository = mock.Mock(wraps=OrderDetailRepositoryImpl())
        self.order_detail_controller = OrderDetailController(
            self.order_detail_repository
        )

    def test_add_order_detail_to_repository_using_controller(self):
        order_detail = build_order_detail()

        self.order_detail_controller.add(order_detail)
        self.order_detail_repository.add.assert_called_with(order_detail)
        self.assertEqual(order_detail.id, 1)

    def test_get_order_detail_from_repository_using_controller(self):
        order_details = build_order_details(count=3)

        self.order_detail_controller.add(order_details[0])
        self.order_detail_controller.add(order_details[1])
        self.order_detail_controller.add(order_details[2])

        found_order_detail3 = self.order_detail_controller.get_by_id(3)

        self.order_detail_repository.get_by_id.assert_called_with(3)
        self.assertEqual(found_order_detail3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_detail(self):
        order_detail1 = build_order_detail()

        self.order_detail_controller.add(order_detail1)

        self.assertRaises(KeyError, self.order_detail_controller.get_by_id, 2)
        self.order_detail_repository.get_by_id.assert_called_with(2)

    def test_get_all_order_details_from_repository_using_controller(self):

        order_details_to_insert = build_order_details(count=4)

        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])
        self.order_detail_controller.add(order_details_to_insert[2])
        self.order_detail_controller.add(order_details_to_insert[3])

        order_details = self.order_detail_controller.get_all()

        self.order_detail_repository.get_all.assert_called_with()

        self.assertEqual(
            order_details,
            [
                order_details_to_insert[0],
                order_details_to_insert[1],
                order_details_to_insert[2],
                order_details_to_insert[3],
            ],
        )

    def test_get_all_order_details_empty_from_repository_through_controller(
        self,
    ):
        order_details = self.order_detail_controller.get_all()
        self.order_detail_repository.get_all.assert_called_with()
        self.assertEqual(order_details, [])

    def test_delete_an_order_detail_from_repository_using_controller(self):
        order_details_to_insert = build_order_details(count=4)
        order_detail_to_delete = build_order_detail(entity_status=Status.ACTIVE)
        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])
        self.order_detail_controller.add(order_details_to_insert[2])
        self.order_detail_controller.add(order_details_to_insert[3])

        self.order_detail_controller.delete_by_id(3, order_detail_to_delete)
        order_details = self.order_detail_controller.get_all()

        self.order_detail_repository.delete_by_id.assert_called_once_with(
            3, order_detail_to_delete
        )

        self.assertEqual(
            order_details,
            [
                order_details_to_insert[0],
                order_details_to_insert[1],
                order_details_to_insert[3],
            ],
        )

    def test_delete_throws_key_error_when_there_are_no_order_details(self):
        order_detail_to_delete = build_order_detail(entity_status=Status.ACTIVE)
        self.assertRaises(
            KeyError,
            self.order_detail_controller.delete_by_id,
            3,
            order_detail_to_delete,
        )
        self.order_detail_repository.delete_by_id.assert_called_with(
            3, order_detail_to_delete
        )

    def test_update_order_detail_from_repository_using_controller(self):
        order_details_to_insert = build_order_details(count=2)

        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])

        order_detail_to_update = build_order_detail(quantity=5)

        self.order_detail_controller.update_by_id(2, order_detail_to_update)
        updated_order_detail = self.order_detail_controller.get_by_id(2)
        order_details = self.order_detail_controller.get_all()

        self.order_detail_repository.update_by_id.assert_called_once_with(
            2, order_detail_to_update
        )

        self.assertEqual(len(order_details), 2)
        self.assertEqual(
            updated_order_detail.quantity,
            order_detail_to_update.quantity,
        )

    def test_get_by_order_detail_id_from_repository_using_controller(self):
        order_1 = build_order(order_id=1)
        product_1 = build_product(product_id=1, name="test product 1")
        product_2 = build_product(product_id=2, name="test product 2")
        order_detail_1 = build_order_detail(
            order_id=order_1.id, product_id=product_1.id, quantity=2
        )
        order_detail_2 = build_order_detail(
            order_id=order_1.id, product_id=product_2.id, quantity=3
        )
        self.order_detail_repository.add(order_detail_1)
        self.order_detail_repository.add(order_detail_2)

        order_details_by_order_detail = self.order_detail_controller.get_by_order_id(
            order_detail_1.id
        )
        self.order_detail_repository.get_by_order_id.assert_called_with(
            order_detail_1.id
        )
