from bson import ObjectId

from src.constants.etl_status import EtlStatus, Service
from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.core.engine.processors.etl.mongo_order_status_history_distribution_etl import (
    UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT,
)
from src.grpc.clients.ea_restaurant_java_etl_grpc_client import (
    EaRestaurantJavaEtlGrpcClient,
)
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl as MongoOrderStatusHistoryRepository,
)

UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT = 1


class JavaEtlMongoOrderStatusHistoriesProcessor(AbstractProcessor):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

        self.mongo_order_status_history_repository = None
        self.ea_restaurant_java_etl_grpc_client = None

    def set_app_context(self, app_context):
        ioc = app_context.ioc
        self.mongo_order_status_history_repository = ioc.get(
            MongoOrderStatusHistoryRepository
        )
        self.ea_restaurant_java_etl_grpc_client = ioc.get(EaRestaurantJavaEtlGrpcClient)

    def process(self, delta_time):
        mongo_order_status_histories = self.mongo_order_status_history_repository.get_order_status_histories_by_service(
            Service.JAVA_ETL,
            EtlStatus.UNPROCESSED,
            limit=UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT,
        )

        if mongo_order_status_histories:
            self.send_mongo_order_status_histories_to_java_etl(
                mongo_order_status_histories
            )

    def send_mongo_order_status_histories_to_java_etl(
        self, mongo_order_status_histories
    ):

        uuids_response = self.ea_restaurant_java_etl_grpc_client.insert_mongo_order_status_histories_from_python_etl(
            mongo_order_status_histories
        )

        uuids = [ObjectId(uuid) for uuid in uuids_response]

        self.mongo_order_status_history_repository.update_batch_to_processed(uuids)
