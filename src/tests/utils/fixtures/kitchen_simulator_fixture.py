from src.core.engine.processors.kitchen_simulator import KitchenSimulator
from src.tests.utils.fixtures.app_engine_processor_context_fixture import (
    build_app_engine_processor_context,
)
from src.tests.utils.fixtures.app_processor_config_fixture import (
    build_app_processor_config,
)


def build_kitchen_simulator(app_processor_config=None, app_context=None):
    kitchen_simulator = KitchenSimulator(
        app_processor_config or build_app_processor_config()
    )
    kitchen_simulator.app_context = app_context or build_app_engine_processor_context()
    return kitchen_simulator


def build_kitchen_simulator_running_once(app_processor_config=None):
    kitchen_simulator = build_kitchen_simulator(
        app_processor_config=app_processor_config
    )

    def after_execute(_app_processor_config, _app_context):
        kitchen_simulator.destroyed = True

    kitchen_simulator.app_processor_config.after_execute = after_execute

    return kitchen_simulator
