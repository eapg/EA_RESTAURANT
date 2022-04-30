from abc import ABCMeta

from src.core.engine.processors.abstract_processor import AbstractProcessor


class KitchenSimulator(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

    def process(self, delta_time):
        print("Waiting orders")
