from abc import ABCMeta
import unittest
from unittest import mock

from src.core.engine.processors.abstract_etl_processor import AbstractEtl
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.mapping_odm_fixtures import build_order_status_history


class TestEtlProcessor(AbstractEtl, metaclass=ABCMeta):
    def __init__(self, app_processor_config=None, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

    def extract_data(self):
        pass

    def transform_data(self, extracted_data):
        pass

    def load_data(self, transformed_data):
        pass


class TestAbstractEtl(unittest.TestCase):
    def setUp(self):
        self.app_processor_config = build_app_processor_config()

        def after_execute(_app_processor_config, _app_context):
            self.test_etl_processor.destroyed = True

        self.app_processor_config.after_execute = after_execute

        self.test_etl_processor = TestEtlProcessor(
            app_processor_config=self.app_processor_config
        )
        self.test_etl_processor.extract_data = mock.Mock()
        self.test_etl_processor.transform_data = mock.Mock()
        self.test_etl_processor.load_data = mock.Mock()

    def test_process_with_not_extracted_data(self):

        self.test_etl_processor.extract_data.return_value = None
        self.test_etl_processor.start()

        self.test_etl_processor.transform_data.assert_not_called()
        self.test_etl_processor.load_data.assert_not_called()

    def test_process_with_extracted_data(self):

        order_status_history_1 = build_order_status_history()

        self.test_etl_processor.extract_data.return_value = [order_status_history_1]
        self.test_etl_processor.start()

        self.test_etl_processor.transform_data.assert_called()
        self.test_etl_processor.load_data.assert_called()
