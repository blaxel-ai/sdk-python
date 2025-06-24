import logging

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import Tracer, get_tracer
from wrapt import wrap_function_wrapper

from blaxel.telemetry.span import SpanManager

logger = logging.getLogger(__name__)


class BlaxelLanggraphInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self):
        return ["langgraph"]

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "0.2.0", tracer_provider)
        # self._patch_gemini(tracer)
        self._patch_tool(tracer)

    def _uninstrument(self, **kwargs):
        import blaxel.langgraph.custom.gemini

        # Restore original methods
        if hasattr(
            blaxel.langgraph.custom.gemini.GeminiRestClient, "_blaxel_original_generate_content"
        ):
            blaxel.langgraph.custom.gemini.GeminiRestClient.generate_content = (
                blaxel.langgraph.custom.gemini.GeminiRestClient._blaxel_original_generate_content
            )
            delattr(
                blaxel.langgraph.custom.gemini.GeminiRestClient, "_blaxel_original_generate_content"
            )

        if hasattr(
            blaxel.langgraph.custom.gemini.GeminiRestClient,
            "_blaxel_original_generate_content_async",
        ):
            blaxel.langgraph.custom.gemini.GeminiRestClient.generate_content_async = blaxel.langgraph.custom.gemini.GeminiRestClient._blaxel_original_generate_content_async
            delattr(
                blaxel.langgraph.custom.gemini.GeminiRestClient,
                "_blaxel_original_generate_content_async",
            )

        if hasattr(
            blaxel.langgraph.custom.gemini.GeminiRestClient,
            "_blaxel_original_stream_generate_content",
        ):
            blaxel.langgraph.custom.gemini.GeminiRestClient.stream_generate_content = blaxel.langgraph.custom.gemini.GeminiRestClient._blaxel_original_stream_generate_content
            delattr(
                blaxel.langgraph.custom.gemini.GeminiRestClient,
                "_blaxel_original_stream_generate_content",
            )

        if hasattr(
            blaxel.langgraph.custom.gemini.GeminiRestClient,
            "_blaxel_original_stream_generate_content_async",
        ):
            blaxel.langgraph.custom.gemini.GeminiRestClient.stream_generate_content_async = blaxel.langgraph.custom.gemini.GeminiRestClient._blaxel_original_stream_generate_content_async
            delattr(
                blaxel.langgraph.custom.gemini.GeminiRestClient,
                "_blaxel_original_stream_generate_content_async",
            )

    def _patch_tool(self, tracer: Tracer):
        def _traced_run(original, instance, args, kwargs):
            attributes = {
                "tool.type": "langgraph",
                "span.type": "tool.call",
                **SpanManager.get_default_attributes(),
            }
            with tracer.start_span("langgraph.tool", attributes=attributes) as span:
                try:
                    result = original(*args, **kwargs)
                    span.set_attribute("tool.name", result.name)
                    return result
                except Exception as e:
                    span.set_attribute("tool.error", str(e))
                    raise

        async def _traced_arun(original, instance, args, kwargs):
            attributes = {
                "tool.type": "langgraph",
                "span.type": "tool.call",
                **SpanManager.get_default_attributes(),
            }
            with tracer.start_span("langgraph.tool", attributes=attributes) as span:
                try:
                    result = await original(*args, **kwargs)
                    span.set_attribute("tool.name", result.name)
                    return result
                except Exception as e:
                    span.set_attribute("tool.error", str(e))
                    raise

        wrap_function_wrapper("langchain_core.tools", "BaseTool.run", _traced_run)
        wrap_function_wrapper("langchain_core.tools", "BaseTool.arun", _traced_arun)
        wrap_function_wrapper("langchain_core.tools", "BaseTool.arun", _traced_arun)
