from src.core.engine.app_processor_config import AppProcessorConfig


def build_app_engine_config(
    id=None, interval=None, on_start=None, on_destroy=None, on_execute=None
):
    app_engine_config = AppProcessorConfig()
    app_engine_config.id = id or "test engine config"
    app_engine_config.interval = interval or 5
    app_engine_config.on_start = on_start
    app_engine_config.on_destroy = on_destroy
    app_engine_config.on_execute = on_execute
    return app_engine_config
