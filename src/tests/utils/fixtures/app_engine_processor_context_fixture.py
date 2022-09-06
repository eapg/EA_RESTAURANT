from src.core.engine import app_engine_processor_context


def build_app_engine_processor_context(processors=None):
    app_engine_processor_context_instance = (
        app_engine_processor_context.AppEngineProcessorContext()
    )
    app_engine_processor_context_instance.processors = processors
    return app_engine_processor_context_instance
