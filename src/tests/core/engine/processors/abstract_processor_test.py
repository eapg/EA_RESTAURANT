import time
import unittest
from abc import ABCMeta
from unittest import mock

from src.core.engine.processors.abstract_processor import AbstractProcessor
from src.tests.utils.fixtures.app_processor_config_fixture import \
    build_app_processor_config


class TestProcessor(AbstractProcessor, metaclass=ABCMeta):
    def __init__(self, app_processor_config=None, app_context=None):
        super().__init__(
            app_processor_config=app_processor_config, app_context=app_context
        )

    def process(self, delta_time):
        print(f"Process executed - Testing {self.app_processor_config.id}")


class TestAbstractProcessor(unittest.TestCase):
    @mock.patch("threading.Thread.__init__")
    def test_processor_default_parameters(self, test_thread_init):
        app_processor_config = build_app_processor_config(on_start=None)
        test_processor = TestProcessor(app_processor_config)
        test_thread_init.assert_called_once()

        self.assertEqual(
            test_processor.app_processor_config.id, app_processor_config.id
        )
        self.assertFalse(test_processor.paused)
        self.assertFalse(test_processor.destroyed)

    @mock.patch.object(TestProcessor, "process")
    def test_processor_process_method_was_called(self, mocked_test_processor_process):
        app_processor_config = build_app_processor_config()
        test_processor = TestProcessor(app_processor_config)

        def after_execute(_app_processor_config, _app_context):
            test_processor.destroyed = True

        app_processor_config.after_execute = after_execute
        test_processor.start()
        test_processor.join()

        mocked_test_processor_process.assert_called_once()
        self.assertTrue(test_processor.destroyed)
        self.assertFalse(test_processor.is_alive())

    def test_processor_on_destroy(self):
        mocked_on_destroy = mock.Mock()
        app_processor_config = build_app_processor_config(on_destroy=mocked_on_destroy)
        test_processor = TestProcessor(app_processor_config)

        def after_execute(_app_processor_config, _app_context):
            test_processor.destroyed = True

        app_processor_config.after_execute = after_execute
        test_processor.start()
        test_processor.join()

        mocked_on_destroy.assert_called_once()
        mocked_on_destroy.assert_called_with(app_processor_config, None)
        self.assertTrue(test_processor.destroyed)
        self.assertFalse(test_processor.is_alive())

    def test_processor_on_start(self):
        mocked_on_start = mock.Mock()
        app_processor_config = build_app_processor_config(on_start=mocked_on_start)
        test_processor = TestProcessor(app_processor_config)

        def after_execute(_app_processor_config, _app_context):
            test_processor.destroyed = True

        app_processor_config.after_execute = after_execute
        test_processor.start()
        test_processor.join()

        mocked_on_start.assert_called_once()
        mocked_on_start.assert_called_with(app_processor_config, None)
        self.assertTrue(test_processor.destroyed)
        self.assertFalse(test_processor.is_alive())

    def test_processor_before_execute(self):
        mocked_before_execute = mock.Mock()
        app_processor_config = build_app_processor_config(
            before_execute=mocked_before_execute
        )
        test_processor = TestProcessor(app_processor_config)

        def after_execute(_app_processor_config, _app_context):
            test_processor.destroyed = True

        app_processor_config.after_execute = after_execute
        test_processor.start()
        test_processor.join()

        mocked_before_execute.assert_called_once()
        mocked_before_execute.assert_called_with(app_processor_config, None)
        self.assertTrue(test_processor.destroyed)
        self.assertFalse(test_processor.is_alive())

    @mock.patch.object(TestProcessor, "process")
    def test_processor_paused(self, mocked_test_processor_process):
        app_processor_config = build_app_processor_config()
        test_processor = TestProcessor(app_processor_config)

        flag_map = {"interrupted": False}

        def after_execute(_app_processor_config, _app_context):
            test_processor.paused = True
            flag_map["interrupted"] = True

        app_processor_config.after_execute = mock.Mock(wraps=after_execute)
        test_processor.start()

        loop_limit = 5

        while not flag_map["interrupted"] and loop_limit > 0:
            loop_limit -= 1
            time.sleep(0.2)

        app_processor_config.after_execute.assert_called_once()
        app_processor_config.after_execute.assert_called_with(
            app_processor_config, None
        )
        mocked_test_processor_process.assert_called_once()

        self.assertTrue(test_processor.paused)
        self.assertTrue(test_processor.is_alive())

        test_processor.destroyed = True
        test_processor.join()

    @mock.patch.object(TestProcessor, "process")
    def test_processor_last_execution_time(self, mocked_test_processor_process):
        app_processor_config = build_app_processor_config()
        test_processor = TestProcessor(app_processor_config)

        last_execution_time_opportunities_map = {"max": 2, "last_execution_times": []}

        def before_execute(_app_processor_config, _app_context):
            last_execution_time_opportunities_map["last_execution_times"].append(
                test_processor.last_execution_time
            )

            if last_execution_time_opportunities_map["max"] > 0:
                last_execution_time_opportunities_map["max"] -= 1
            else:
                test_processor.destroyed = True

        app_processor_config.before_execute = before_execute
        test_processor.start()
        test_processor.join()

        mocked_test_processor_process.assert_has_calls(
            [
                mock.call(
                    last_execution_time_opportunities_map["last_execution_times"][1]
                    - last_execution_time_opportunities_map["last_execution_times"][0]
                ),
                mock.call(
                    last_execution_time_opportunities_map["last_execution_times"][2]
                    - last_execution_time_opportunities_map["last_execution_times"][1]
                ),
                mock.call(
                    test_processor.last_execution_time
                    - last_execution_time_opportunities_map["last_execution_times"][2]
                ),
            ]
        )
        self.assertTrue(test_processor.destroyed)
        self.assertFalse(test_processor.is_alive())
