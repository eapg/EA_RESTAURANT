from unittest import TestCase, mock

from src.core.engine.app_engine_processor import AppEngineProcessor


class AppEngineProcessorIntegrationTest(TestCase):
    def test_process_run(self):
        app_engine_processor = AppEngineProcessor()
        kitchen_simulator = app_engine_processor.app_context.processors[0]

        def after_execute(_app_processor_config, _app_context):
            kitchen_simulator.destroyed = True

        kitchen_simulator.app_processor_config.after_execute = mock.Mock(
            wraps=after_execute
        )
        kitchen_simulator.start = mock.Mock(wraps=kitchen_simulator.start)
        kitchen_simulator.process = mock.Mock(wraps=kitchen_simulator.process)
        kitchen_simulator.app_processor_config.interval = 0.01

        app_engine_processor.start()
        app_engine_processor.app_context.processors[0].join()

        kitchen_simulator.start.assert_called_once()
        kitchen_simulator.app_processor_config.after_execute.assert_called_once()
        kitchen_simulator.process.assert_called_once()
        self.assertTrue(kitchen_simulator.destroyed)
