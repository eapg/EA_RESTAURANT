from src.core.engine.processors import kitchen_simulator
from src.tests.utils.fixtures import app_engine_processor_context_fixture
from src.tests.utils.fixtures import app_processor_config_fixture


def build_kitchen_simulator(app_processor_config=None, app_context=None):
    kitchen_simulator_instance = kitchen_simulator.KitchenSimulator(
        app_processor_config
        or app_processor_config_fixture.build_app_processor_config()
    )
    kitchen_simulator_instance.app_context = (
        app_context
        or app_engine_processor_context_fixture.build_app_engine_processor_context()
    )
    return kitchen_simulator_instance


def build_kitchen_simulator_running_once(app_processor_config=None):
    kitchen_simulator_instance = build_kitchen_simulator(
        app_processor_config=app_processor_config
    )

    def after_execute(_app_processor_config, _app_context):
        kitchen_simulator.destroyed = True

    kitchen_simulator_instance.app_processor_config.after_execute = after_execute

    return kitchen_simulator_instance
