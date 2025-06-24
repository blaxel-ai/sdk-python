import json
import logging

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import Tracer, get_tracer

import blaxel.core.agents
import blaxel.core.jobs
from blaxel.telemetry.span import SpanManager

logger = logging.getLogger(__name__)


class BlaxelCoreInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self):
        return []

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "0.2.0", tracer_provider)
        self._patch_agent(tracer)
        self._patch_job(tracer)
        self._patch_tools(tracer)

    def _uninstrument(self, **kwargs):
        # Optionally restore original methods
        pass

    def _patch_agent(self, tracer: Tracer):
        orig_run = blaxel.core.agents.BlAgent.run

        def traced_run(self, *args, **kwargs):
            attributes = {
                "agent.name": self.name,
                "agent.args": str(args),
                "span.type": "agent.run",
                **SpanManager.get_default_attributes(),
            }
            with tracer.start_span(self.name, attributes=attributes) as span:
                try:
                    result = orig_run(self, *args, **kwargs)
                    span.set_attribute("agent.run.result", result)
                    return result
                except Exception as e:
                    span.set_attribute("agent.run.error", str(e))
                    raise

        blaxel.core.agents.BlAgent.run = traced_run

    def _patch_job(self, tracer: Tracer):
        orig_run = blaxel.core.jobs.BlJob.run

        def traced_run(self, *args, **kwargs):
            attributes = {
                "job.name": self.name,
                "span.type": "job.run",
                **SpanManager.get_default_attributes(),
            }
            with tracer.start_span(self.name, attributes=attributes) as span:
                try:
                    result = orig_run(self, *args, **kwargs)
                    span.set_attribute("job.run.result", result)
                    return result
                except Exception as e:
                    span.set_attribute("job.run.error", str(e))
                    raise

        blaxel.core.jobs.BlJob.run = traced_run

    def _patch_tools(self, tracer: Tracer):
        # Patch PersistentWebSocket.list_tools
        orig_list_tools = blaxel.core.tools.PersistentWebSocket.list_tools

        async def traced_list_tools(self, *args, **kwargs):
            span_attributes = {
                "tool.server": self.url,
                "tool.server_name": self.name,
                "span.type": "tool.list",
                **SpanManager.get_default_attributes(),
            }
            with tracer.start_span(self.name, attributes=span_attributes):
                result = await orig_list_tools(self, *args, **kwargs)
                # Optionally: span.set_attribute("tool.list.result", str(result))
                return result

        blaxel.core.tools.PersistentWebSocket.list_tools = traced_list_tools

        # Patch convert_mcp_tool_to_blaxel_tool to wrap tool calls
        orig_convert = blaxel.core.tools.convert_mcp_tool_to_blaxel_tool

        def traced_convert_mcp_tool_to_blaxel_tool(websocket_client, name, url, tool):
            Tool = orig_convert(websocket_client, name, url, tool)
            orig_coroutine = Tool.coroutine
            orig_sync_coroutine = Tool.sync_coroutine

            async def traced_coroutine(*args, **kwargs):
                span_attributes = {
                    "tool.name": tool.name,
                    "tool.args": json.dumps(kwargs),
                    "tool.server": url,
                    "tool.server_name": name,
                    "span.type": "tool.call",
                    **SpanManager.get_default_attributes(),
                }
                logger.info(span_attributes)
                with tracer.start_span("blaxel-tool-call", attributes=span_attributes):
                    return await orig_coroutine(*args, **kwargs)

            def traced_sync_coroutine(*args, **kwargs):
                span_attributes = {
                    "tool.name": tool.name,
                    "tool.args": json.dumps(kwargs),
                    "tool.server": url,
                    "tool.server_name": name,
                    "span.type": "tool.call",
                    **SpanManager.get_default_attributes(),
                }
                with tracer.start_span("blaxel-tool-call", attributes=span_attributes):
                    return orig_sync_coroutine(*args, **kwargs)

            Tool.coroutine = traced_coroutine
            Tool.sync_coroutine = traced_sync_coroutine
            return Tool

        blaxel.core.tools.convert_mcp_tool_to_blaxel_tool = traced_convert_mcp_tool_to_blaxel_tool
