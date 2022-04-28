import unittest
from unittest.mock import patch

from src.core.engine.app_engine_processor import AppEngineProcessor
from src.tests.utils.fixtures.app_processor_config_fixture import \
    build_app_engine_config
from src.tests.utils.fixtures.kitchen_simulator_fixture import \
    build_kitchen_simulator


class TestAppEngineProcessor(unittest.TestCase):
    @patch(
        "src.core.engine.app_engine_processor.AppProcessorConfig",
        return_value=build_app_engine_config(),
    )
    def test_mock_in_app_context(self, mocked_app_processor_config):

        app_engine_processor = AppEngineProcessor()
        self.assertEqual(len(app_engine_processor.app_context.processors), 1)
        self.assertEqual(
            app_engine_processor.app_context.processors[0].app_processor_config.id,
            "test engine config",
        )

    @patch(
        "src.core.engine.app_engine_processor.KitchenSimulator.start",
        return_value=build_kitchen_simulator(),
    )
    def test_start_in_context_run_once(self, mocked_kitchen_simulator):

        app_engine_processor = AppEngineProcessor()
        app_engine_processor.start()
        mocked_kitchen_simulator._mock_return_value.start.assert_called()
