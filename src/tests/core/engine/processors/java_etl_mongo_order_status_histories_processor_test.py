from unittest import mock

from bson import ObjectId

from src.core.engine.processors.java_etl_mongo_order_status_histories_processor import (
    JavaEtlMongoOrderStatusHistoriesProcessor,
)
from src.tests.base_env_config_test import BaseEnvConfigTest
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import (
    build_order_status_history,
)


class JavaEtlMongoOrderStatusHistoriesProcessorTest(BaseEnvConfigTest):
    def setUp(self):
        super().setUp()
        self.app_engine_config = build_app_processor_config()
        self.java_etl_mongo_order_status_history_processor = (
            JavaEtlMongoOrderStatusHistoriesProcessor(self.app_engine_config)
        )
        self.java_etl_mongo_order_status_history_processor.mongo_order_status_history_repository = (
            mock.Mock()
        )
        self.java_etl_mongo_order_status_history_processor.ea_restaurant_java_etl_grpc_client = (
            mock.Mock()
        )

    def test_send_mongo_order_status_histories_to_java_etl(self):
        java_grpc_client = (
            self.java_etl_mongo_order_status_history_processor.ea_restaurant_java_etl_grpc_client
        )
        mongo_order_status_repository = (
            self.java_etl_mongo_order_status_history_processor.mongo_order_status_history_repository
        )
        mongo_order_status_1 = build_order_status_history(id="63656f20f2a8a6a247ae31cc")
        mongo_order_status_2 = build_order_status_history(id="63656f20f2a8a6a247ae31cd")
        mongo_order_status_histories = [mongo_order_status_1, mongo_order_status_2]

        java_grpc_client.insert_mongo_order_status_histories_from_python_etl.return_value = [
            "63656f20f2a8a6a247ae31cc",
            "63656f20f2a8a6a247ae31cd",
        ]

        self.java_etl_mongo_order_status_history_processor.send_mongo_order_status_histories_to_java_etl(
            mongo_order_status_histories
        )

        java_grpc_client.insert_mongo_order_status_histories_from_python_etl.assert_called_with(
            mongo_order_status_histories
        )
        mongo_order_status_repository.update_batch_to_processed.assert_called_with(
            [ObjectId("63656f20f2a8a6a247ae31cc"), ObjectId("63656f20f2a8a6a247ae31cd")]
        )
