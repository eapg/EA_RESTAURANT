from bson import ObjectId

from src.api.controllers.order_status_history_controller import (
    OrderStatusHistoryController,
)
from src.constants.audit import InternalUsers
from src.core.engine.processors.etl.abstract_etl_processor import AbstractEtl
from src.lib.entities.sqlalchemy_orm_mapping import (
    OrderStatusHistory as SqlalchemyOrderStatusHistory,
)
from src.lib.repositories.impl_no_sql.order_status_history_repository_impl import (
    OrderStatusHistoryRepositoryImpl as MongoOrderStatusHistoryRepository,
)
from src.utils.etl_util import (
    convert_mongo_order_status_history_to_postgres_order_status_history,
)
from src.utils.order_status_history_util import update_last_order_status_history

"""
This class MongoToPostgresqlOrderStatusHistory is an etl between mongo and postgres. It will migrate the data store 
from mongo to postgres every so often. The mongo Db will be the only source of true of order status histories. It will 
replicate data to postgres which could be used to generate reports and other uses determined by the users. The 
initial data in postgres order status histories table was truncate whereby the mongo collection is empty at the 
beginning.
"""


class MongoToPostgresqlOrderStatusHistoryEtl(AbstractEtl):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

        self.order_status_history_controller = None
        self.mongo_order_status_history_repository = None

    def set_app_context(self, app_context):
        ioc = app_context.ioc

        self.order_status_history_controller = ioc.get(OrderStatusHistoryController)
        self.mongo_order_status_history_repository = ioc.get(
            MongoOrderStatusHistoryRepository
        )

    def extract_data(self):

        order_status_histories_from_mongo = (
            self.mongo_order_status_history_repository.get_unprocessed_order_status_histories()
        )

        return order_status_histories_from_mongo

    def transform_data(self, extracted_data):
        transformed_data = []

        for mongo_order_status_history in extracted_data:
            postgresql_order_status_history = SqlalchemyOrderStatusHistory()
            postgresql_order_status_history_with_mongo_data = (
                convert_mongo_order_status_history_to_postgres_order_status_history(
                    mongo_order_status_history, postgresql_order_status_history
                )
            )

            transformed_data.append(postgresql_order_status_history_with_mongo_data)

        return transformed_data

    def load_data(self, transformed_data):
        mongo_uuids = [
            ObjectId(order_status_history.mongo_order_status_history_uuid)
            for order_status_history in transformed_data
        ]
        order_ids = [
            order_status_history_1.order_id
            for order_status_history_1 in transformed_data
        ]

        last_order_status_histories = self.order_status_history_controller.last_order_status_histories_by_order_ids(
            order_ids
        )

        if last_order_status_histories:

            updated_last_order_status_histories = update_last_order_status_history(
                last_order_status_histories, transformed_data, InternalUsers.ETL.value
            )
            self.order_status_history_controller.insert_new_or_updated_batch_order_status_histories(
                updated_last_order_status_histories
            )

        self.order_status_history_controller.insert_new_or_updated_batch_order_status_histories(
            transformed_data
        )

        self.mongo_order_status_history_repository.update_batch_to_processed(
            mongo_uuids
        )
