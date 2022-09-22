from abc import abstractmethod, ABCMeta

from src.core.engine.processors.abstract_processor import AbstractProcessor


class AbstractEtl(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

    def process(self, delta_time):
        data_extracted = self.extract_data()
        if data_extracted:
            data_transformed = self.transform_data(data_extracted)
            self.load_data(data_transformed)

    @abstractmethod
    def extract_data(self):
        pass

    @abstractmethod
    def transform_data(self, extracted_data):
        pass

    @abstractmethod
    def load_data(self, transformed_data):
        pass
