import unittest
from unittest import mock

from src.core.engine.app_engine_processor import AppEngineProcessor
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)
from src.tests.utils.fixtures.kitchen_simulator_fixture import (
    build_kitchen_simulator_running_once,
)


class TestAppEngineProcessor(unittest.TestCase):
    def setUp(self):
        self.app_processor_config = build_app_processor_config()
        self.app_processor_config_patch = mock.patch(
            "src.core.engine.app_engine_processor.AppProcessorConfig",
            return_value=self.app_processor_config,
        )

        self.kitchen_simulator = build_kitchen_simulator_running_once(
            app_processor_config=self.app_processor_config
        )
        self.mocked_kitchen_simulator = mock.Mock(wraps=self.kitchen_simulator)
        self.kitchen_simulator_patch = mock.patch(
            "src.core.engine.app_engine_processor.KitchenSimulator",
            return_value=self.mocked_kitchen_simulator,
        )

        self.app_processor_config_patch.start()
        self.kitchen_simulator_patch.start()

    def test_engine_app_context(self):
        app_engine_processor = AppEngineProcessor()
        self.assertEqual(len(app_engine_processor.app_context.processors), 1)
        self.assertEqual(
            app_engine_processor.app_context.processors[0].app_processor_config._mock_wraps.id,
            self.app_processor_config.id,
        )

    def test_engine_start(self):
        app_engine_processor = AppEngineProcessor()
        app_engine_processor.start()
        self.kitchen_simulator.join()
        self.mocked_kitchen_simulator.start.assert_called_once()
