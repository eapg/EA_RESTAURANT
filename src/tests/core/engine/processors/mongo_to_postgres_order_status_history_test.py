from unittest import mock

from src.constants.audit import InternalUsers
from src.core.engine.processors.etl.abstract_etl_processor import AbstractEtl
from src.core.engine.processors.etl.mongo_to_postgresql_order_status_history_etl import (
    MongoToPostgresqlOrderStatusHistoryEtl,
)
from src.tests.lib.repositories.mongo_engine_base_repository_impl_test import (
    MongoEngineBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import (
    build_order_status_history as mongo_build_order_status_history,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import build_order_status_history


class MongoToPostgresOrderStatusHistoryTest(MongoEngineBaseRepositoryTestCase):
    def after_base_setup(self):
        self.app_config = build_app_processor_config()

        self.mongo_to_postgres_etl = MongoToPostgresqlOrderStatusHistoryEtl(AbstractEtl)

        etl = self.mongo_to_postgres_etl
        etl.app_processor_config = self.app_config
        etl.order_status_history_controller = mock.Mock()
        etl.order_status_history_controller.add = mock.Mock()
        etl.mongo_order_status_history_repository = mock.Mock()
        etl.mongo_order_status_history_repository.update_batch_to_processed = (
            mock.Mock()
        )

    def test_extract_data_successfully(self):
        etl = self.mongo_to_postgres_etl
        etl.transform_data = mock.Mock()
        etl.load_data = mock.Mock()

        def after_execute(_app_processor_config, _app_context):
            etl.destroyed = True

        etl.app_processor_config.after_execute = after_execute

        etl.start()
        mongo_repository = etl.mongo_order_status_history_repository
        mongo_repository.get_unprocessed_order_status_histories.assert_called()

    @mock.patch(
        "src.core.engine.processors.mongo_to_postgresql_order_status_history."
        + "convert_mongo_order_status_history_to_postgres_order_status_history"
    )
    def test_transform_data_successfully(self, mocked_convert_mongo_to_postgres):

        self.mongo_to_postgres_etl.load_data = mock.Mock()
        self.mongo_to_postgres_etl.extract_data = mock.Mock()

        mongo_order_status_history_1 = mongo_build_order_status_history()
        mongo_order_status_history_2 = mongo_build_order_status_history()

        self.mongo_to_postgres_etl.extract_data.return_value = [
            mongo_order_status_history_1,
            mongo_order_status_history_2,
        ]

        def after_execute(_app_processor_config, _app_context):
            self.mongo_to_postgres_etl.destroyed = True

        self.mongo_to_postgres_etl.app_processor_config.after_execute = after_execute

        self.mongo_to_postgres_etl.start()
        mocked_convert_mongo_to_postgres.has_called_with(
            mock.call(mongo_order_status_history_1),
            mock.call(mongo_order_status_history_2),
        )

    @mock.patch(
        "src.core.engine.processors.mongo_to_postgresql_order_status_history."
        + "update_last_order_status_history"
    )
    def test_load_data_successfully(self, mocked_update_last_order_status_history):

        last_order_status_history_1 = build_order_status_history()
        last_order_status_history_2 = build_order_status_history()

        self.mongo_to_postgres_etl.extract_data = mock.Mock()

        self.mongo_to_postgres_etl.transform_data = mock.Mock()

        order_status_history_1 = build_order_status_history()
        order_status_history_1.mongo_order_status_history_uuid = (
            "632b1cbdd411e2e0c2ac80e6"
        )

        order_status_history_2 = build_order_status_history()
        order_status_history_2.mongo_order_status_history_uuid = (
            "632b1cbdd411e2e0c2ac80e7"
        )

        etl = self.mongo_to_postgres_etl
        controller = etl.order_status_history_controller
        controller.last_order_status_histories_by_order_ids.return_value = [
            last_order_status_history_1,
            last_order_status_history_2,
        ]

        self.mongo_to_postgres_etl.transform_data.return_value = [
            order_status_history_1,
            order_status_history_2,
        ]

        def after_execute(_app_processor_config, _app_context):
            self.mongo_to_postgres_etl.destroyed = True

        self.mongo_to_postgres_etl.app_processor_config.after_execute = after_execute

        self.mongo_to_postgres_etl.start()
        mocked_update_last_order_status_history.assert_called_with(
            [last_order_status_history_1, last_order_status_history_2],
            [
                order_status_history_1,
                order_status_history_2,
            ],
            InternalUsers.ETL.value,
        )
        self.mongo_to_postgres_etl.mongo_order_status_history_repository.add.has_called_with(
            [mock.call(order_status_history_1), mock.call(order_status_history_2)]
        )

        etl = self.mongo_to_postgres_etl
        repository = etl.mongo_order_status_history_repository
        repository.update_batch_to_processed.has_called_with(
            mock.call("632b1cbdd411e2e0c2ac80e6"), mock.call("632b1cbdd411e2e0c2ac80e7")
        )
