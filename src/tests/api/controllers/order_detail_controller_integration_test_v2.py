from src.api.controllers.order_detail_controller import OrderDetailController

from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_order,
    build_order_detail,
    build_order_details,
)
from src.tests.utils.test_util import get_order_detail_repository_with_session_patched


class OrderDetailIngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.order_detail_repository = get_order_detail_repository_with_session_patched(
            self
        )
        self.order_detail_controller = OrderDetailController(
            self.order_detail_repository
        )

    def test_add_order_detail_to_repository_using_controller(self):

        order_detail = build_order_detail()

        self.order_detail_controller.add(order_detail)
        self.order_detail_repository.add.assert_called_with(order_detail)

    def test_get_order_detail_from_repository_using_controller(self):

        order_details = build_order_details(count=3)

        self.order_detail_controller.add(order_details[0])
        self.order_detail_controller.add(order_details[1])
        self.order_detail_controller.add(order_details[2])
        self.order_detail_repository.get_by_id.return_value = order_details[2]
        found_order_detail2 = self.order_detail_controller.get_by_id(2)

        self.order_detail_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_order_detail2.id, 2)

    def test_get_all_inventories_from_repository_using_controller(self):

        order_details_to_insert = build_order_details(count=4)

        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])
        self.order_detail_controller.add(order_details_to_insert[2])
        self.order_detail_controller.add(order_details_to_insert[3])
        self.order_detail_repository.get_all.return_value = order_details_to_insert
        inventories = self.order_detail_controller.get_all()

        self.order_detail_repository.get_all.assert_called_with()

        self.assertEqual(
            inventories,
            [
                order_details_to_insert[0],
                order_details_to_insert[1],
                order_details_to_insert[2],
                order_details_to_insert[3],
            ],
        )

    def test_get_all_inventories_empty_from_repository_through_controller(
        self,
    ):
        self.order_detail_repository.get_all.return_value = []
        inventories = self.order_detail_controller.get_all()
        self.order_detail_repository.get_all.assert_called_with()
        self.assertEqual(inventories, [])

    def test_delete_an_order_detail_from_repository_using_controller(self):

        order_details_to_insert = build_order_details(count=4)
        order_detail_to_delete = build_order_detail()
        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])
        self.order_detail_controller.add(order_details_to_insert[2])
        self.order_detail_controller.add(order_details_to_insert[3])

        self.order_detail_controller.delete_by_id(3, order_detail_to_delete)
        self.order_detail_repository.get_all.return_value = [
            order_details_to_insert[0],
            order_details_to_insert[1],
            order_details_to_insert[3],
        ]
        inventories = self.order_detail_controller.get_all()

        self.order_detail_repository.delete_by_id.assert_called_once_with(
            3, order_detail_to_delete
        )

        self.assertEqual(
            inventories,
            [
                order_details_to_insert[0],
                order_details_to_insert[1],
                order_details_to_insert[3],
            ],
        )

    def test_update_order_detail_from_repository_using_controller(self):

        order_details_to_insert = build_order_details(count=2)

        self.order_detail_controller.add(order_details_to_insert[0])
        self.order_detail_controller.add(order_details_to_insert[1])

        order_detail_to_update = build_order_detail()
        self.order_detail_controller.update_by_id(2, order_detail_to_update)
        self.order_detail_repository.get_by_id.return_value = order_detail_to_update
        updated_order_detail = self.order_detail_controller.get_by_id(2)
        self.order_detail_repository.get_all.return_value = order_details_to_insert
        inventories = self.order_detail_controller.get_all()

        self.order_detail_repository.update_by_id.assert_called_once_with(
            2, order_detail_to_update
        )

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_order_detail.updated_by,
            order_detail_to_update.updated_by,
        )

    def test_get_by_order_id_from_repository_using_controller(self):

        order_1 = build_order(order_id=1)

        order_detail_1 = build_order_detail(order_id=order_1.id)
        order_detail_2 = build_order_detail(order_id=order_1.id)
        self.order_detail_repository.add(order_detail_1)
        self.order_detail_repository.add(order_detail_2)
        self.order_detail_repository.get_by_order_id.return_value = [
            order_detail_1,
            order_detail_2,
        ]
        order_details_by_order_detail = self.order_detail_controller.get_by_order_id(
            order_detail_1.id
        )
        self.order_detail_repository.get_by_order_id.assert_called_with(
            order_detail_1.id
        )
        self.assertEqual(
            order_details_by_order_detail, [order_detail_1, order_detail_2]
        )
