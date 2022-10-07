import unittest

from src.constants.audit import Status
from src.lib.repositories.impl.order_detail_repository_impl import \
    OrderDetailRepositoryImpl
from src.tests.utils.fixtures.order_detail_fixture import (build_order_detail,
                                                           build_order_details)
from src.tests.utils.fixtures.product_fixture import build_product


class OrderDetailRepositoryImplTestCase(unittest.TestCase):
    def test_add_order_detail_successfully(self):
        order_detail = build_order_detail()
        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_detail)

        self.assertEqual(order_detail.id, 1)

    def test_get_order_detail_successfully(self):
        order_details = build_order_details(count=3)

        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_details[0])
        order_detail_repository.add(order_details[1])
        order_detail_repository.add(order_details[2])

        found_order_detail3 = order_detail_repository.get_by_id(3)

        self.assertEqual(found_order_detail3.id, 3)

    def test_get_throws_key_error_for_non_existing_order_detail(self):
        order_detail1 = build_order_detail()

        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_detail1)

        self.assertRaises(KeyError, order_detail_repository.get_by_id, 2)

    def test_get_all_order_details_successfully(self):
        order_details_to_insert = build_order_details(count=5)

        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_details_to_insert[0])
        order_detail_repository.add(order_details_to_insert[1])
        order_detail_repository.add(order_details_to_insert[2])
        order_detail_repository.add(order_details_to_insert[3])
        order_detail_repository.add(order_details_to_insert[4])

        order_details = order_detail_repository.get_all()

        self.assertEqual(
            order_details,
            [
                order_details_to_insert[0],
                order_details_to_insert[1],
                order_details_to_insert[2],
                order_details_to_insert[3],
                order_details_to_insert[4],
            ],
        )

    def test_get_all_order_details_empty_successfully(self):
        order_detail_repository = OrderDetailRepositoryImpl()

        order_details = order_detail_repository.get_all()

        self.assertEqual(order_details, [])

    def test_delete_an_order_detail_successfully(self):
        order_details_to_insert = build_order_details(count=3)
        order_detail_to_delete = build_order_detail(entity_status=Status.ACTIVE)
        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_details_to_insert[0])
        order_detail_repository.add(order_details_to_insert[1])
        order_detail_repository.add(order_details_to_insert[2])

        order_detail_repository.delete_by_id(2, order_detail_to_delete)

        order_details = order_detail_repository.get_all()

        self.assertEqual(
            order_details,
            [order_details_to_insert[0], order_details_to_insert[2]],
        )

    def test_delete_throws_key_error_when_there_are_no_order_details(self):
        order_detail_repository = OrderDetailRepositoryImpl()
        order_detail_to_delete = build_order_detail(entity_status=Status.ACTIVE)
        self.assertRaises(
            KeyError, order_detail_repository.delete_by_id, 2, order_detail_to_delete
        )

    def test_update_order_detail_successfully(self):
        order_details_to_insert = build_order_details(count=2)

        order_detail_repository = OrderDetailRepositoryImpl()

        order_detail_repository.add(order_details_to_insert[0])
        order_detail_repository.add(order_details_to_insert[1])

        order_detail_to_update = build_order_detail(quantity=5)

        order_detail_repository.update_by_id(2, order_detail_to_update)
        updated_order_detail = order_detail_repository.get_by_id(2)
        order_details = order_detail_repository.get_all()

        self.assertEqual(len(order_details), 2)
        self.assertEqual(
            updated_order_detail.quantity,
            order_detail_to_update.quantity,
        )

    def test_get_by_order_id(self):
        order_1 = build_order_detail(order_id=1)
        product_1 = build_product(product_id=1, name="test product 1")
        product_2 = build_product(product_id=2, name="test product 2")
        order_detail_1 = build_order_detail(
            order_id=order_1.id, product_id=product_1.id, quantity=2
        )
        order_detail_2 = build_order_detail(
            order_id=order_1.id, product_id=product_2.id, quantity=3
        )
        order_detail_repository = OrderDetailRepositoryImpl()
        order_detail_repository.add(order_detail_1)
        order_detail_repository.add(order_detail_2)

        order_details_by_order_id = order_detail_repository.get_by_order_id(order_1.id)
        self.assertEqual(len(order_details_by_order_id), 2)
        self.assertEqual(
            order_details_by_order_id,
            [order_detail_1, order_detail_2],
        )
