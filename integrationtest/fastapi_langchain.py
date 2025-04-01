import asyncio
import time
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from blaxel.instrumentation.span import SpanManager
from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def main():
    async with bl_tools(["blaxel-search"]) as t:
        tools = t.to_langchain()
        model = await bl_model("gpt-4o-mini").to_langchain()
        agent = create_react_agent(model=model, tools=tools, prompt="You are a helpful assistant that can answer questions and help with tasks.")

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
            with SpanManager("blaxel-langchain").create_active_span("agent-request", {}) as span:
                body = await request.json()
                result = await agent.ainvoke({"messages": [HumanMessage(body.get("inputs", ""))]})
                span.set_attribute("agent.result", result["messages"][-1].content)

                return Response(
                    result["messages"][-1].content,
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
