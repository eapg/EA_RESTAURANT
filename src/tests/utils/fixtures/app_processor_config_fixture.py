from src.core.engine import app_processor_config


def build_app_processor_config(
    id=None,
    interval=None,
    on_start=None,
    on_destroy=None,
    before_execute=None,
    after_execute=None,
):
    app_processor_config_instance = app_processor_config.AppProcessorConfig(
        id or "config_test", interval or 0.01
    )
    app_processor_config_instance.on_start = on_start
    app_processor_config_instance.on_destroy = on_destroy
    app_processor_config_instance.before_execute = before_execute
    app_processor_config_instance.after_execute = after_execute
    return app_processor_config_instance
