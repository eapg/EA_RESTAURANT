from unittest.mock import patch
from unittest import TestCase
from src.core.engine.app_engine_processor import AppEngineProcessor
from src.tests.utils.fixtures.kitchen_simulator_fixture import build_kitchen_simulator


class AppEngineProcessorIntegrationTest(TestCase):

    @patch(
        "src.core.engine.app_engine_processor.KitchenSimulator.process",
        return_value=build_kitchen_simulator(),
    )
    def test_process_run(self, mocked_kitchen_simulator_process):

        app_engine_processor = AppEngineProcessor()
        app_engine_processor.start()
        mocked_kitchen_simulator_process.assert_called()
