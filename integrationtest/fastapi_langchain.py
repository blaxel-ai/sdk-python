import traceback
from logging import getLogger
from time import time

from fastapi.responses import JSONResponse

logger = getLogger(__name__)
total = time()
start = time()

from contextlib import asynccontextmanager

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from blaxel.instrumentation.span import SpanManager
from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger.info(f"Loaded blaxel in {round(time() - start, 4)} seconds")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server running on port 1338")
    yield
    logger.info("Server shutting down")

start = time()
app = FastAPI(lifespan=lifespan)
logger.info(f"Created app in {round(time() - start, 4)} seconds")
start = time()
app.add_middleware(CorrelationIdMiddleware)
logger.info(f"Added correlation id middleware in {round(time() - start, 4)} seconds")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    response: Response = await call_next(request)

    process_time = (time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    rid_header = response.headers.get("X-Request-Id")
    request_id = rid_header or response.headers.get("X-Blaxel-Request-Id")
    logger.info(f"{request.method} {request.url.path} {response.status_code} {formatted_process_time}ms rid={request_id}")

    return response

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, e: Exception):
    logger.error(f"Error on request {request.method} {request.url.path}: {e}")

    # Get the full traceback information
    tb_str = traceback.format_exception(type(e), e, e.__traceback__)
    logger.error(f"Stacktrace: {''.join(tb_str)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": str(e)}),
    )


@app.post("/")
async def handle_request(request: Request):
    start = time()
    tools = await bl_tools(["blaxel-search", "mymcp"]).to_langchain()
    logger.info(f"Loaded tools in {round(time() - start, 4)} seconds")
    start = time()
    logger.info(f"Converted tools to langchain in {round(time() - start, 4)} seconds")
    start = time()
    model = await bl_model("gpt-4o-mini").to_langchain()
    logger.info(f"Retrieved model in langchain in {round(time() - start, 4)} seconds")
    start = time()
    agent = create_react_agent(model=model, tools=tools, prompt="You are a helpful assistant that can answer questions and help with tasks.")
    logger.info(f"Create agent in {round(time() - start, 4)} seconds")
    with SpanManager("blaxel-langchain").create_active_span("agent-request", {}) as span:
        body = await request.json()
        result = await agent.ainvoke({"messages": [HumanMessage(body.get("inputs", ""))]})
        span.set_attribute("agent.result", result["messages"][-1].content)

        return Response(
            result["messages"][-1].content,
            media_type="text/plain"
        )

start = time()
FastAPIInstrumentor.instrument_app(app)
logger.info(f"Instrumented app in {round(time() - start, 4)} seconds")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")