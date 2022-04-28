from src.core.engine.processors.kitchen_simulator import KitchenSimulator
from src.tests.utils.fixtures.app_engine_processor_context_fixture import \
    build_app_engine_processor_context
from src.tests.utils.fixtures.app_processor_config_fixture import \
    build_app_engine_config


def build_kitchen_simulator(app_processor_config=None, app_context=None):
    kitchen_simulator = KitchenSimulator()
    kitchen_simulator.app_processor_config = (
        app_processor_config or build_app_engine_config()
    )
    kitchen_simulator.app_context = app_context or build_app_engine_processor_context()
    return kitchen_simulator
