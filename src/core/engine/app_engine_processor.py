# thread manager
from injector import Injector

from src.core.di_config import DiProviders
from src.core.engine.app_engine_processor_context import AppEngineProcessorContext
from src.core.engine.app_processor_config import AppProcessorConfig
from src.core.engine.processors.etl.mongo_order_status_history_distribution_etl import (
    MongoOrderStatusHistoryDistributionEtl,
)
from src.core.engine.processors.java_etl_mongo_order_status_histories_processor import (
    JavaEtlMongoOrderStatusHistoriesProcessor,
)
from src.core.engine.processors.kitchen_simulator import (
    KitchenSimulator,
    initialize_kitchen_simulator,
)
from src.core.engine.processors.etl.mongo_to_postgresql_order_status_history_etl import (
    MongoToPostgresqlOrderStatusHistoryEtl,
)
from src.core.order_manager import OrderManager
from src.env_config import get_env_config_instance


class AppEngineProcessor:
    def __init__(self):

        env_config = get_env_config_instance()
        ioc = Injector(DiProviders)

        java_etl_mongo_order_status_history_config = AppProcessorConfig(
            id="java_etl_mongo_order_status_history",
            interval=env_config.java_etl_interval,
        )
        mongo_order_status_history_distribution_etl_config = AppProcessorConfig(
            id="mongo_order_status_history_distribution_etl",
            interval=env_config.distribution_etl_interval,
        )
        mongo_to_postgres_etl_config = AppProcessorConfig(
            id="mongo_to_postgres_etl",
            interval=env_config.etl_interval,
        )
        kitchen_simulator_config = AppProcessorConfig(
            id="kitchen_simulator_test",
            interval=env_config.kitchen_simulator_interval,
            order_manager=OrderManager(),
            on_start=initialize_kitchen_simulator,
        )
        java_etl_mongo_order_status_history = JavaEtlMongoOrderStatusHistoriesProcessor(
            java_etl_mongo_order_status_history_config
        )
        mongo_order_status_history_distribution_etl = (
            MongoOrderStatusHistoryDistributionEtl(
                mongo_order_status_history_distribution_etl_config
            )
        )
        mongo_to_postgres_etl = MongoToPostgresqlOrderStatusHistoryEtl(
            mongo_to_postgres_etl_config
        )
        kitchen_simulator = KitchenSimulator(kitchen_simulator_config)
        self.app_context = AppEngineProcessorContext(
            processors=[
                kitchen_simulator,
                mongo_order_status_history_distribution_etl,
                java_etl_mongo_order_status_history,
                mongo_to_postgres_etl
            ],
            ioc=ioc,
        )
        java_etl_mongo_order_status_history.set_app_context(self.app_context)
        mongo_order_status_history_distribution_etl.set_app_context(self.app_context)
        kitchen_simulator.set_app_context(self.app_context)
        mongo_to_postgres_etl.set_app_context(self.app_context)

    # method to Start thread process
    def start(self):
        if self.app_context.processors:
            [processor.start() for processor in self.app_context.processors]
        else:
            raise "No processors found"


# function to run the simulation of the AppEngineProcessor()
def app_engine_processor_start():

    app_engine_processor = AppEngineProcessor()
    app_engine_processor.start()


if __name__ == "__main__":
    app_engine_processor_start()
