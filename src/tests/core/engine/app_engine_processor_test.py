import unittest
from unittest import mock

from src.core.engine.app_engine_processor import AppEngineProcessor
from src.tests.utils.fixtures.app_processor_config_fixture import \
    build_app_processor_config
from src.tests.utils.fixtures.kitchen_simulator_fixture import \
    build_kitchen_simulator_running_once


class TestAppEngineProcessor(unittest.TestCase):
    @mock.patch(
        "src.core.engine.app_engine_processor.AppProcessorConfig",
        return_value=build_app_processor_config(),
    )
    @mock.patch(
        "src.core.engine.app_engine_processor.KitchenSimulator",
        return_value=build_kitchen_simulator_running_once(),
    )
    def test_engine_app_context(
        self, _mocked_kitchen_simulator, _mocked_app_processor_config
    ):
        app_processor_config = build_app_processor_config()
        app_engine_processor = AppEngineProcessor()
        self.assertEqual(len(app_engine_processor.app_context.processors), 1)
        self.assertEqual(
            app_engine_processor.app_context.processors[0].app_processor_config.id,
            app_processor_config.id,
        )

    @mock.patch("src.core.engine.app_engine_processor.AppProcessorConfig")
    @mock.patch("src.core.engine.app_engine_processor.KitchenSimulator.start")
    def test_engine_start(
        self, mocked_kitchen_simulator_start, _mocked_app_processor_config
    ):
        app_engine_processor = AppEngineProcessor()
        app_engine_processor.start()
        mocked_kitchen_simulator_start.assert_called_once()
