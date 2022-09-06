# thread manager

from src.core.engine import app_engine_processor_context
from src.core.engine import app_processor_config
from src.core.engine.processors import kitchen_simulator


class AppEngineProcessor:
    def __init__(self):
        kitchen_simulator_config = app_processor_config.AppProcessorConfig("kitchen_simulator_test", 0.2)
        kitchen_simulator_instance = kitchen_simulator.KitchenSimulator(kitchen_simulator_config)
        self.app_context = app_engine_processor_context.AppEngineProcessorContext(processors=[kitchen_simulator_instance])

        kitchen_simulator_instance.app_context = self.app_context

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
