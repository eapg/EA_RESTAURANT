# thread manager

from src.core.engine.app_engine_processor_context import AppEngineProcessorContext
from src.core.engine.app_processor_config import AppProcessorConfig
from src.core.engine.processors.kitchen_simulator import KitchenSimulator


class AppEngineProcessor:
    def __init__(self):
        kitchen_simulator_config = AppProcessorConfig("kitchen_simulator_test", 10)
        kitchen_simulator = KitchenSimulator(kitchen_simulator_config)
        self.app_context = AppEngineProcessorContext(processors=[kitchen_simulator])

        kitchen_simulator.app_context = self.app_context

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
