import time
import traceback
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic_ai import Agent, CallToolsNode
from pydantic_ai.messages import ToolCallPart
from pydantic_ai.models import ModelSettings

from blaxel.instrumentation.span import SpanManager
from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

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
    start = time.time()
    tools = await bl_tools(["blaxel-search"]).to_pydantic()
    logger.info(f"Loaded tools in {round(time.time() - start, 4)} seconds")

    start = time.time()
    model = await bl_model("gpt-4o-mini").to_pydantic()
    logger.info(f"Retrieved model in {round(time.time() - start, 4)} seconds")

    with SpanManager("blaxel-pydantic").create_active_span("agent-request", {}) as span:
        body = await request.json()
        if not "inputs" in body:
            raise HTTPException(status_code=400, detail="inputs is required")

        agent = Agent(model=model, tools=tools, model_settings=ModelSettings(temperature=0))
        async with agent.iter(body["inputs"]) as agent_run:
            async for node in agent_run:
                if isinstance(node, CallToolsNode):
                    for part in node.model_response.parts:
                        if isinstance(part, ToolCallPart):
                            logger.info(f"Tool call: {part}")
                        else:
                            logger.info(f"Response: {part}")
                            response = part.content
        return Response(
            response,
            media_type="text/plain"
        )

FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")
