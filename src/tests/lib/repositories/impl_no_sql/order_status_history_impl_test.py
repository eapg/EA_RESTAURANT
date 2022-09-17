from unittest import mock

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.lib.entities.mongo_engine_odm_mapping import OrderStatusHistory
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import (
    build_order_status_histories,
    build_order_status_history,
)
from src.tests.lib.repositories.mongo_engine_base_repository_impl_test import (
    MongoEngineBaseRepositoryTestCase,
)


class OrderStatusHistoryRepositoryImplTest(MongoEngineBaseRepositoryTestCase):
    def after_base_setup(self):
        self.order_status_history_repository = OrderStatusHistoryRepositoryImpl(
            self.mocked_mongo_engine_connection
        )

    @mock.patch.object(OrderStatusHistory, "save")
    def test_add_to_repository_successfully(self, mocked_save):
        order_status_history_1 = build_order_status_history()
        self.order_status_history_repository.add(order_status_history_1)
        mocked_save.assert_called_with()

    @mock.patch.object(OrderStatusHistory, "objects")
    def test_get_by_id_successfully(self, mocked_objects):

        order_status_history_1 = build_order_status_history()
        self.order_status_history_repository.add(order_status_history_1)
        mocked_objects.get.return_value = order_status_history_1
        order_status_history_returned = self.order_status_history_repository.get_by_id(
            1
        )

        mocked_objects.get.assert_called_with(id=1, entity_status="ACTIVE")
        self.assertEqual(order_status_history_1, order_status_history_returned)

    @mock.patch.object(OrderStatusHistory, "objects")
    def test_get_all_successfully(self, mocked_objects):
        order_status_histories = build_order_status_histories(count=3)

        self.order_status_history_repository.add(order_status_histories[0])
        self.order_status_history_repository.add(order_status_histories[1])
        self.order_status_history_repository.add(order_status_histories[2])
        mocked_objects.return_value = [
            order_status_histories[0],
            order_status_histories[1],
            order_status_histories[2],
        ]
        order_status_histories_returned = self.order_status_history_repository.get_all()
        mocked_objects.assert_called_with(entity_status="ACTIVE")
        self.assertEqual(
            order_status_histories_returned,
            [
                order_status_histories[0],
                order_status_histories[1],
                order_status_histories[2],
            ],
        )

    @mock.patch(
        "src.lib.repositories.impl_no_sql.order_status_history_repository_impl.datetime"
    )
    @mock.patch.object(OrderStatusHistory, "objects")
    def test_deleted_by_id_successfully(self, mocked_objects, mocked_datetime):
        order_status_history_to_delete = build_order_status_history(
            entity_status=Status.DELETED.value, updated_by=2
        )
        self.order_status_history_repository.delete_by_id(
            1, order_status_history_to_delete
        )
        mocked_objects.assert_called_with(id=1)
        mocked_objects().update_one.assert_called_with(
            entity_status=order_status_history_to_delete.entity_status,
            updated_date=mocked_datetime.now(),
            updated_by=order_status_history_to_delete.updated_by,
        )

    @mock.patch.object(OrderStatusHistory, "objects")
    def test_update_by_id_successfully(self, mocked_objects):
        order_status_history_to_update = build_order_status_history(updated_by=5)

        self.order_status_history_repository.update_by_id(
            1, order_status_history_to_update
        )
        mocked_objects.get.assert_called_with(id=1)

    @mock.patch.object(OrderStatusHistory, "objects")
    def test_get_by_order_id_successfully(self, mocked_objects):
        order_status_history_1 = build_order_status_history(order_id=5)
        self.order_status_history_repository.add(order_status_history_1)
        mocked_objects.return_value = order_status_history_1
        order_status_history_returned = (
            self.order_status_history_repository.get_by_order_id(5)
        )
        mocked_objects.assert_called_with(order_id=5, entity_status=Status.ACTIVE.value)
        self.assertEqual(order_status_history_returned, order_status_history_1)

    @mock.patch.object(OrderStatusHistory, "objects")
    def test_get_last_order_status_history_successfully(self, mocked_objects):
        order_status_history_1 = build_order_status_history(order_id=3)
        self.order_status_history_repository.add(order_status_history_1)
        mocked_objects.return_value.order_by.return_value.limit.return_value.__getitem__.return_value = (
            order_status_history_1
        )
        last_order_status_history = (
            self.order_status_history_repository.get_last_status_history_by_order_id(3)
        )
        mocked_objects.assert_called_with(order_id=3)
        mocked_objects.return_value.order_by.assert_called_with("-from_time")
        mocked_objects.return_value.order_by.return_value.limit.assert_called_with(1)
        self.assertEqual(order_status_history_1, last_order_status_history)

    @mock.patch.object(OrderStatusHistory, "save")
    def test_set_next_order_Status_history_successfully(self, mocked_save):
        order_status_history_1 = build_order_status_history(
            order_id=2, from_status=OrderStatus.NEW_ORDER.name
        )
        self.order_status_history_repository.add(order_status_history_1)
        self.order_status_history_repository.get_last_status_history_by_order_id = (
            mock.Mock()
        )
        self.order_status_history_repository.get_last_status_history_by_order_id.return_value = (
            order_status_history_1
        )
        self.order_status_history_repository.set_next_status_history_by_order_id(
            2, OrderStatus.IN_PROCESS.name
        )
        mocked_save.assert_called_with()
        self.assertEqual(len(mocked_save.mock_calls), 3)