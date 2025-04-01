import asyncio
import time
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from llama_index.core.agent.workflow import (AgentOutput, ReActAgent,
                                             ToolCallResult)
from llama_index.core.workflow import Context
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from blaxel.instrumentation.span import SpanManager
from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def main():
    async with bl_tools(["blaxel-search"]) as t:
        tools = t.to_llamaindex()
        model = await bl_model("gpt-4o-mini").to_llamaindex()

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Server running on port 1338")
            yield
            logger.info("Server shutting down")

        app = FastAPI(lifespan=lifespan)
        app.add_middleware(CorrelationIdMiddleware)

        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            start_time = time.time()

            response: Response = await call_next(request)

            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            rid_header = response.headers.get("X-Request-Id")
            request_id = rid_header or response.headers.get("X-Blaxel-Request-Id")
            logger.info(f"{request.method} {request.url.path} {response.status_code} {formatted_process_time}ms rid={request_id}")

            return response

        @app.post("/")
        async def handle_request(request: Request):
            with SpanManager("blaxel-llamaindex").create_active_span("agent-request", {}) as span:
                body = await request.json()
                agent = ReActAgent(llm=model, tools=tools, system_prompt="You are a helpful assistant. Maximum number of tool call is 1.")
                context = Context(agent)
                handler = agent.run(body.get("inputs", ""), ctx=context)
                async for ev in handler.stream_events():
                    if isinstance(ev, ToolCallResult):
                        logger.info(f"Call {ev.tool_name} with {ev.tool_kwargs}")
                response: AgentOutput = await handler
                span.set_attribute("agent.result", response.response.blocks[-1].text)
                return Response(
                    response.response.blocks[-1].text,
                    media_type="text/plain"
                )

        FastAPIInstrumentor.instrument_app(app)

        server_config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=1338,
            log_level="critical"
        )
        server = uvicorn.Server(server_config)
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
