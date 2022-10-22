import unittest
from unittest import mock

from injector import Injector

from src.constants.etl_status import EtlStatus
from src.constants.order_status import OrderStatus
from src.core.di_config import DiProviders
from src.core.engine.processors.abstract_etl_processor import AbstractEtl
from src.core.engine.processors.mongo_to_postgresql_order_status_history import (
    MongoToPostgresqlOrderStatusHistory,
)
from src.tests.lib.repositories.mongo_engine_base_repository_impl_test import (
    MongoEngineBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.app_engine_processor_context_fixture import (
    build_app_engine_processor_context,
)
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import (
    build_order_status_history as mongo_build_order_status_history,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import build_order_status_history


@unittest.skip("skipped")
class MongoToPostgresOrderStatusHistoryIntegrationTest(
    MongoEngineBaseRepositoryTestCase
):
    def after_base_setup(self):

        self.mocked_sqlalchemy_session = mock.Mock()

        self.mocked_sqlalchemy_session.get_bind.return_value.begin.return_value.__enter__ = (
            mock.Mock()
        )
        self.mocked_sqlalchemy_session.get_bind.return_value.begin.return_value.__exit__ = (
            mock.Mock()
        )

        self.mocked_sqlalchemy_session.begin.return_value.__enter__ = mock.Mock()
        self.mocked_sqlalchemy_session.begin.return_value.__exit__ = mock.Mock()

        self.mocked_sqlalchemy_engine = mock.Mock()

        ioc = Injector(DiProviders)
        self.app_config = build_app_processor_config()
        self.app_context = build_app_engine_processor_context()
        self.app_context.ioc = ioc

        self.mongo_to_postgres_etl = MongoToPostgresqlOrderStatusHistory(AbstractEtl)
        self.mongo_to_postgres_etl.app_processor_config = self.app_config

        self.mongo_to_postgres_etl.set_app_context(self.app_context)

        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.order_status_history_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.mongo_to_postgres_etl.order_status_history_controller.session = (
            self.mocked_sqlalchemy_engine
        )
        self.mocked_creation_session_path.start()

        self.mongo_to_postgres_etl.extract_data = mock.Mock(
            wraps=self.mongo_to_postgres_etl.extract_data
        )
        self.mongo_to_postgres_etl.transform_data = mock.Mock(
            wraps=self.mongo_to_postgres_etl.transform_data
        )
        self.mongo_to_postgres_etl.load_data = mock.Mock(
            wraps=self.mongo_to_postgres_etl.load_data
        )

    def test_extract_data_successfully(self):

        mongo_order_status_history_1 = mongo_build_order_status_history()
        mongo_order_status_history_1.etl_status = EtlStatus.UNPROCESSED.value
        self.mongo_to_postgres_etl.mongo_order_status_history_repository.add(
            mongo_order_status_history_1
        )

        def after_execute(_app_processor_config, _app_context):
            self.mongo_to_postgres_etl.destroyed = True

        self.mongo_to_postgres_etl.app_processor_config.after_execute = after_execute
        self.mongo_to_postgres_etl.start()
        self.mongo_to_postgres_etl.extract_data.assert_called()

    def test_transform_data_successfully(self):

        mongo_order_status_history_1 = mongo_build_order_status_history()
        mongo_order_status_history_1.id = "632cbbe58a488dac10a734e2"
        mongo_order_status_history_1.etl_status = EtlStatus.UNPROCESSED.value
        self.mongo_to_postgres_etl.extract_data.return_value = [
            mongo_order_status_history_1
        ]

        def after_execute(_app_processor_config, _app_context):
            self.mongo_to_postgres_etl.destroyed = True

        self.mongo_to_postgres_etl.app_processor_config.after_execute = after_execute
        self.mongo_to_postgres_etl.start()
        self.mongo_to_postgres_etl.transform_data.assert_called_with(
            [mongo_order_status_history_1]
        )

    def test_load_data_successfully(self):

        mongo_order_status_history_1 = mongo_build_order_status_history()
        mongo_order_status_history_1.id = "632cbbe58a488dac10a734e2"
        mongo_order_status_history_1.etl_status = EtlStatus.UNPROCESSED.value

        order_status_history = build_order_status_history()
        order_status_history.id = 5
        order_status_history.updated_by = 2
        order_status_history.from_status = OrderStatus.NEW_ORDER.name
        self.mongo_to_postgres_etl.extract_data.return_value = [
            mongo_order_status_history_1
        ]
        self.mongo_to_postgres_etl.transform_data.return_value = [order_status_history]

        def after_execute(_app_processor_config, _app_context):
            self.mongo_to_postgres_etl.destroyed = True

        self.mongo_to_postgres_etl.app_processor_config.after_execute = after_execute
        self.mongo_to_postgres_etl.start()

        self.mongo_to_postgres_etl.load_data.assert_called_with([order_status_history])
