from src.core.engine.app_engine_processor_context import AppEngineProcessorContext


def build_app_engine_processor_context(processors=None):
    app_engine_processor_context = AppEngineProcessorContext()
    app_engine_processor_context.processors = processors
    return app_engine_processor_context
