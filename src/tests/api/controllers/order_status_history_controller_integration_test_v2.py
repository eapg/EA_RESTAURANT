from unittest import mock

from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.constants.order_status import OrderStatus
from src.lib.repositories.impl_v2.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl,
)
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    build_inventories,
    build_order,
    build_order_status_history,
    build_order_status_histories,
)


class OrderStatusHistoryIngredientRepositoryControllerIntegrationTestCase(
    SqlAlchemyBaseRepositoryTestCase
):
    def after_base_setup(self):
        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.order_status_history_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.order_status_history_repository = mock.Mock(
            wraps=OrderStatusHistoryRepositoryImpl(self.mocked_sqlalchemy_engine)
        )
        self.mocked_creation_session_path.start()

        self.order_status_history_controller = OrderStatusHistoryController(
            self.order_status_history_repository
        )

    def test_add_order_status_history_to_repository_using_controller(self):

        order_status_history = build_order_status_history()

        self.order_status_history_controller.add(order_status_history)
        self.order_status_history_repository.add.assert_called_with(
            order_status_history
        )

    def test_get_order_status_history_from_repository_using_controller(self):

        order_status_histories = build_inventories(count=3)

        self.order_status_history_controller.add(order_status_histories[0])
        self.order_status_history_controller.add(order_status_histories[1])
        self.order_status_history_controller.add(order_status_histories[2])
        self.order_status_history_repository.get_by_id.return_value = (
            order_status_histories[2]
        )
        found_order_status_history2 = self.order_status_history_controller.get_by_id(2)

        self.order_status_history_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_order_status_history2.id, 1)

    def test_get_all_inventories_from_repository_using_controller(self):

        order_status_histories_to_insert = build_order_status_histories(count=4)

        self.order_status_history_controller.add(order_status_histories_to_insert[0])
        self.order_status_history_controller.add(order_status_histories_to_insert[1])
        self.order_status_history_controller.add(order_status_histories_to_insert[2])
        self.order_status_history_controller.add(order_status_histories_to_insert[3])
        self.order_status_history_repository.get_all.return_value = (
            order_status_histories_to_insert
        )
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

    def test_get_all_inventories_empty_from_repository_through_controller(
        self,
    ):
        self.order_status_history_repository.get_all.return_value = []
        order_status_histories = self.order_status_history_controller.get_all()
        self.order_status_history_repository.get_all.assert_called_with()
        self.assertEqual(order_status_histories, [])

    def test_delete_an_order_status_history_from_repository_using_controller(self):

        order_status_histories = build_inventories(count=4)

        order_status_history_to_delete = build_order_status_history()
        self.order_status_history_controller.add(order_status_histories[0])
        self.order_status_history_controller.add(order_status_histories[1])
        self.order_status_history_controller.add(order_status_histories[2])
        self.order_status_history_controller.add(order_status_histories[3])

        self.order_status_history_controller.delete_by_id(
            3, order_status_history_to_delete
        )
        self.order_status_history_repository.get_all.return_value = [
            order_status_histories[0],
            order_status_histories[1],
            order_status_histories[3],
        ]
        inventories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.delete_by_id.assert_called_once_with(
            3, order_status_history_to_delete
        )

        self.assertEqual(
            inventories,
            [
                order_status_histories[0],
                order_status_histories[1],
                order_status_histories[3],
            ],
        )

    def test_update_order_status_history_from_repository_using_controller(self):

        order_status_histories = build_inventories(count=2)

        self.order_status_history_controller.add(order_status_histories[0])
        self.order_status_history_controller.add(order_status_histories[1])
        order_status_history_to_update = build_order_status_history()
        self.order_status_history_controller.update_by_id(
            2, order_status_history_to_update
        )
        self.order_status_history_repository.get_by_id.return_value = (
            order_status_history_to_update
        )
        updated_order_status_history = self.order_status_history_controller.get_by_id(2)
        self.order_status_history_repository.get_all.return_value = (
            order_status_histories
        )
        inventories = self.order_status_history_controller.get_all()

        self.order_status_history_repository.update_by_id.assert_called_once_with(
            2, order_status_history_to_update
        )

        self.assertEqual(len(inventories), 2)
        self.assertEqual(
            updated_order_status_history.updated_by,
            order_status_history_to_update.updated_by,
        )

    def test_get_by_order_id_from_repository_using_controller(self):

        order_1 = build_order(order_id=1)
        order_status_history_1 = build_order_status_history(order_id=order_1.id)
        order_status_history_2 = build_order_status_history()
        self.order_status_history_controller.add(order_status_history_1)
        self.order_status_history_controller.add(order_status_history_2)
        self.order_status_history_repository.get_by_order_id.return_value = (
            order_status_history_1
        )
        _order_status_histories_returned = (
            self.order_status_history_controller.get_by_order_id(order_1.id)
        )
        self.order_status_history_repository.get_by_order_id.assert_called_with(
            order_1.id
        )

    def test_set_next_status_history_by_order_id_from_repository_using_controller(self):

        order_1 = build_order(order_id=1, status=OrderStatus.NEW_ORDER)
        self.order_status_history_controller.set_next_status_history_by_order_id(
            order_1.id, order_1.status
        )

        self.order_status_history_repository.set_next_status_history_by_order_id.assert_called_with(
            order_1.id, order_1.status
        )
