from src.core.engine.app_processor_config import AppProcessorConfig


def build_app_processor_config(
    app_processor_config_id=None,
    interval=None,
    on_start=None,
    on_destroy=None,
    before_execute=None,
):
    app_processor_config = AppProcessorConfig("config_test", 1)
    app_processor_config.id = app_processor_config_id or "config_test"
    app_processor_config.interval = interval or 0.01
    app_processor_config.on_start = on_start
    app_processor_config.on_destroy = on_destroy
    app_processor_config.before_execute = before_execute
    return app_processor_config
