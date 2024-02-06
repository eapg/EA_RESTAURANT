import unittest
from unittest import mock

import mongoengine

from src.constants.etl_status import Service, EtlStatus
from src.constants.order_status import OrderStatus
from src.core.engine.processors.etl.abstract_etl_processor import AbstractEtl
from src.core.engine.processors.etl.mongo_order_status_history_distribution_etl import (
    MongoOrderStatusHistoryDistributionEtl,
    UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT,
)
from src.lib.entities.mongo_engine_odm_mapping import OrderStatusHistory
from src.tests.lib.repositories.mongo_engine_base_repository_impl_test import (
    MongoEngineBaseRepositoryTestCase,
)
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import (
    build_order_status_history as mongo_build_order_status_history,
)


class MongoOrderStatusHistoryDistributionEtlTest(MongoEngineBaseRepositoryTestCase):
    def after_base_setup(self):
        self.app_config = build_app_processor_config()
        self.mongo_order_status_distribution_etl = (
            MongoOrderStatusHistoryDistributionEtl(AbstractEtl)
        )
        self.mongo_order_status_distribution_etl.app_processor_config = self.app_config
        self.mongo_order_status_distribution_etl.mongo_order_status_history_repository = (
            mock.Mock()
        )

    def test_extract_data_successfully(self):
        mongo_order_status_distribution_etl = self.mongo_order_status_distribution_etl
        mongo_order_status_distribution_etl.transform_data = mock.Mock()
        mongo_order_status_distribution_etl.load_data = mock.Mock()

        def after_execute(_app_processor_config, _app_context):
            mongo_order_status_distribution_etl.destroyed = True

        mongo_order_status_distribution_etl.app_processor_config.after_execute = (
            after_execute
        )
        mongo_order_status_distribution_etl.start()
        mongo_repository = (
            mongo_order_status_distribution_etl.mongo_order_status_history_repository
        )
        mongo_repository.get_order_status_histories_by_service.assert_called_with(
            Service.UNASSIGNED,
            etl_status=EtlStatus.UNPROCESSED,
            limit=UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT,
        )

    def test_transform_data_successfully(self):
        self.mongo_order_status_distribution_etl.load_data = mock.Mock()
        self.mongo_order_status_distribution_etl.transform_data = mock.Mock()
        self.mongo_order_status_distribution_etl.extract_data = mock.Mock()

        mongo_order_status_history_1 = mongo_build_order_status_history(
            service=Service.UNASSIGNED
        )
        mongo_order_status_history_2 = mongo_build_order_status_history(
            service=Service.UNASSIGNED
        )

        self.mongo_order_status_distribution_etl.extract_data.return_value = [
            mongo_order_status_history_1,
            mongo_order_status_history_2,
        ]

        def after_execute(_app_processor_config, _app_context):
            self.mongo_order_status_distribution_etl.destroyed = True

        self.mongo_order_status_distribution_etl.app_processor_config.after_execute = (
            after_execute
        )

        self.mongo_order_status_distribution_etl.start()
        self.mongo_order_status_distribution_etl.transform_data.assert_called_with(
            [mongo_order_status_history_1, mongo_order_status_history_2]
        )

    def test_load_data_successfully(self):

        mongo_order_status_history_1 = mongo_build_order_status_history(
            service=Service.PYTHON_ETL
        )
        mongo_order_status_history_2 = mongo_build_order_status_history(
            service=Service.JAVA_ETL
        )

        transformed_data = {
            Service.PYTHON_ETL: [mongo_order_status_history_1],
            Service.JAVA_ETL: [mongo_order_status_history_2],
        }

        self.mongo_order_status_distribution_etl.extract_data = mock.Mock()
        self.mongo_order_status_distribution_etl.load_data = mock.Mock()
        self.mongo_order_status_distribution_etl.transform_data = mock.Mock()

        self.mongo_order_status_distribution_etl.transform_data.return_value = (
            transformed_data
        )

        def after_execute(_app_processor_config, _app_context):
            self.mongo_order_status_distribution_etl.destroyed = True

        self.mongo_order_status_distribution_etl.app_processor_config.after_execute = (
            after_execute
        )
        self.mongo_order_status_distribution_etl.start()
        self.mongo_order_status_distribution_etl.load_data.assert_called_with(
            transformed_data
        )

    def test_extract_data_is_converting_from_queryset_to_list(self):
        mongo_order_status_history_1 = mongo_build_order_status_history()
        mongo_order_status_history_2 = mongo_build_order_status_history()
        mongo_order_status_iterable = iter(
            [mongo_order_status_history_1, mongo_order_status_history_2]
        )
        empty_set = OrderStatusHistory.objects.none()
        mongo_order_status_distribution_etl = self.mongo_order_status_distribution_etl

        mongo_repository = (
            mongo_order_status_distribution_etl.mongo_order_status_history_repository
        )
        mongo_repository.get_order_status_histories_by_service.return_value = (
            mongo_order_status_iterable
        )
        extracted_data = mongo_order_status_distribution_etl.extract_data()
        self.assertEqual(
            extracted_data, [mongo_order_status_history_1, mongo_order_status_history_2]
        )
        self.assertEqual(type(extracted_data), list)
