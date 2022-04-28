import time
import unittest
from abc import ABCMeta
from datetime import datetime
from unittest.mock import Mock, patch,MagicMock

from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.tests.utils.fixtures.app_engine_processor_context_fixture import \
    build_app_engine_processor_context
from src.tests.utils.fixtures.app_processor_config_fixture import \
    build_app_engine_config


class ChildProcessor(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config=None, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

    def process(self, delta_time):
        print("process execute")


class TestAbstractProcessor(unittest.TestCase):

    @patch("threading.Thread.__init__", return_value=None)
    def test_initialization_parameters(self, test_thread_init):

        app_engine_config = build_app_engine_config(
            id="test config", interval=10, on_start=None
        )
        app_engine_processor_context = build_app_engine_processor_context([])
        test_class = ChildProcessor(app_engine_config, app_engine_processor_context)
        # test thread init was call
        test_thread_init.assert_called_once()

        # test app engine config
        self.assertEqual(test_class.app_processor_config.id, app_engine_config.id)
        #test app engine processor context
        self.assertEqual(test_class.app_context.processors, app_engine_processor_context.processors)

        #test self pause is false
        self.assertEqual(test_class.pause, False)

        #test self destroy is false
        self.assertEqual(test_class.destroy, False)

    @patch("src.tests.core.engine.processors.abstract_processor_test.datetime.now", return_value=datetime(2000, 1, 1, 0, 0, 0))
    def test_last_execution_time(self, mock_time):

        print(datetime.now())

    @patch.object(ChildProcessor, "process")
    def test_process_method_was_call_with(self, mocked_child_processor_process):
        app_engine_config = build_app_engine_config(id="test config", interval=10)
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        mocked_child_processor_process.assert_called_with(test_class.delta_time)

    def test_on_start_set_once(self):
        mock_function = Mock(wraps=lambda: print("on started"))
        app_engine_config = build_app_engine_config(
            id="test config", interval=10, on_start=mock_function
        )
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        mock_function.assert_called_once()

    def test_on_execute_set_everytime_process_run(self):
        mock_function = Mock(wraps=lambda: print("on execute"))
        app_engine_config = build_app_engine_config(
            id="test config", interval=10, on_execute=mock_function
        )
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        mock_function.assert_called()

    def test_thread_destroy(self):
        app_engine_config = build_app_engine_config(id="test config", interval=10)
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        self.assertTrue(test_class.is_alive())
        test_class.destroy = True
        time.sleep(15)
        self.assertFalse(test_class.is_alive())

    def test_on_destroy_when_destroy_set_true(self):
        mock_function = Mock(wraps=lambda: print("on destroy"))
        app_engine_config = build_app_engine_config(
            id="test config", interval=10, on_destroy=mock_function
        )
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        self.assertTrue(test_class.is_alive())
        test_class.destroy = True
        time.sleep(15)
        self.assertFalse(test_class.is_alive())

    @patch.object(ChildProcessor, "process")
    def test_set_pause_true(self, mocked_child_processor_process):
        app_engine_config = build_app_engine_config(id="test config", interval=10)
        test_class = ChildProcessor(app_engine_config)
        test_class.pause = True
        test_class.start()
        mocked_child_processor_process.assert_not_called()

    @patch.object(time, "sleep")
    def test_sleep_was_call_with(self, mocked_time_sleep):

        app_engine_config = build_app_engine_config(id="test config", interval=10)
        test_class = ChildProcessor(app_engine_config)
        test_class.start()
        mocked_time_sleep.assert_called_with(test_class.app_processor_config.interval)
