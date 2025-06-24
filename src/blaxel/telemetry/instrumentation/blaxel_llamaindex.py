from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.llamaindex.utils import (
    _with_tracer_wrapper,
    process_request,
    process_response,
    start_as_current_span_async,
)
from opentelemetry.semconv_ai import SpanAttributes, TraceloopSpanKindValues
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

TO_INSTRUMENT = [
    {
        "class": "FunctionTool",
        "v9_module": "llama_index.tools.function_tool",
        "v10_module": "llama_index.core.tools.function_tool",
        "v10_legacy_module": "llama_index.legacy.tools.function_tool",
    },
    {
        "class": "QueryEngineTool",
        "v9_module": "llama_index.tools.query_engine",
        "v10_module": "llama_index.core.tools.query_engine",
        "v10_legacy_module": "llama_index.legacy.tools.query_engine",
    },
]


class BlaxelLlamaIndexInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self):
        return ["llama_index"]

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "0.2.0", tracer_provider)

        for module in TO_INSTRUMENT:
            try:
                package_version("llama-index-core")
                self._instrument_module(module["v10_module"], module["class"], tracer)
                self._instrument_module(module["v10_legacy_module"], module["class"], tracer)

            except PackageNotFoundError:
                self._instrument_module(module["v9_module"], module["class"], tracer)

    def _uninstrument(self, **kwargs):
        pass

    def _instrument_module(self, module_name, class_name, tracer):
        wrap_function_wrapper(module_name, f"{class_name}.call", query_wrapper(tracer))
        wrap_function_wrapper(module_name, f"{class_name}.acall", aquery_wrapper(tracer))


@_with_tracer_wrapper
def query_wrapper(tracer, wrapped, instance, args, kwargs):
    name = instance.__class__.__name__
    with tracer.start_as_current_span(f"{name}.tool") as span:
        span.set_attribute(
            SpanAttributes.TRACELOOP_SPAN_KIND,
            TraceloopSpanKindValues.TOOL.value,
        )
        span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)

        process_request(span, args, kwargs)
        res = wrapped(*args, **kwargs)
        process_response(span, res)
        return res


@_with_tracer_wrapper
async def aquery_wrapper(tracer, wrapped, instance, args, kwargs):
    name = instance.__class__.__name__
    async with start_as_current_span_async(tracer=tracer, name=f"{name}.tool") as span:
        span.set_attribute(
            SpanAttributes.TRACELOOP_SPAN_KIND,
            TraceloopSpanKindValues.TOOL.value,
        )
        span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)

        process_request(span, args, kwargs)
        res = await wrapped(*args, **kwargs)
        process_response(span, res)
        return res
