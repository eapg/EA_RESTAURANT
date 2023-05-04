from src.constants.etl_status import Service
from src.core.engine.processors.etl.abstract_etl_processor import AbstractEtl
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl as MongoOrderStatusHistoryRepository,
)

UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT = 1000


class MongoOrderStatusHistoryDistributionEtl(AbstractEtl):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

        self.mongo_order_status_history_repository = None

    def set_app_context(self, app_context):
        ioc = app_context.ioc

        self.mongo_order_status_history_repository = ioc.get(
            MongoOrderStatusHistoryRepository
        )

    def extract_data(self):
        mongo_repository = self.mongo_order_status_history_repository

        unassigned_order_status_histories_from_mongo = (
            mongo_repository.get_order_status_histories_by_service(
                Service.UNASSIGNED, limit=UNASSIGNED_ORDER_STATUS_HISTORIES_LIMIT
            )
        )

        return unassigned_order_status_histories_from_mongo

    def transform_data(self, extracted_data):
        map_assigned_etl_list = {}
        half_length = extracted_data // 2

        assigned_to_python_etl = extracted_data[:half_length]

        map_assigned_etl_list[Service.PYTHON_ETL] = assigned_to_python_etl

        assigned_to_java_etl = extracted_data[half_length:]

        map_assigned_etl_list[Service.JAVA_ETL] = assigned_to_java_etl

        return map_assigned_etl_list

    def load_data(self, transformed_data):
        self._assign_mongo_order_status_histories_to_etl(
            transformed_data, Service.PYTHON_ETL
        )
        self._assign_mongo_order_status_histories_to_etl(
            transformed_data, Service.JAVA_ETL
        )

    def _assign_mongo_order_status_histories_to_etl(self, assigned_etl_map, service):

        assigned_to_etl_ids = [
            mongo_order_status_history.id
            for mongo_order_status_history in assigned_etl_map[service]
        ]
        self.mongo_order_status_history_repository.update_batch_to_assigned_etl(
            assigned_to_etl_ids, service
        )
