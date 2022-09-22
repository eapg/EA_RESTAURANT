# thread manager

from src.core.engine.app_engine_processor_context import AppEngineProcessorContext
from src.core.engine.app_processor_config import AppProcessorConfig
from src.core.engine.processors.kitchen_simulator import (
    KitchenSimulator,
    initialize_kitchen_simulator,
)
from src.core.engine.processors.mongo_to_postgresql_order_status_history import (
    MongoToPostgresqlOrderStatusHistory,
)
from src.core.ioc import get_ioc_instance
from src.core.order_manager import OrderManager


class AppEngineProcessor:
    def __init__(self):
        ioc = get_ioc_instance()
        mongo_to_postgres_etl_config = AppProcessorConfig(
            id="mongo_to_postgres_etl",
            interval=60,
        )
        kitchen_simulator_config = AppProcessorConfig(
            id="kitchen_simulator_test",
            interval=0.2,
            order_manager=OrderManager(),
            on_start=initialize_kitchen_simulator,
        )
        mongo_to_postgres_etl = MongoToPostgresqlOrderStatusHistory(
            mongo_to_postgres_etl_config
        )
        kitchen_simulator = KitchenSimulator(kitchen_simulator_config)
        self.app_context = AppEngineProcessorContext(
            processors=[kitchen_simulator, mongo_to_postgres_etl], ioc=ioc
        )

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
