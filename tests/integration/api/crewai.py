# ruff: noqa: E402

import time
import traceback
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from crewai import Agent, Crew, Task
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from blaxel.crewai import bl_model, bl_tools
from blaxel.telemetry.span import SpanManager

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
    formatted_process_time = f"{process_time:.2f}"
    rid_header = response.headers.get("X-Request-Id")
    request_id = rid_header or response.headers.get("X-Blaxel-Request-Id")
    logger.info(
        f"{request.method} {request.url.path} {response.status_code} {formatted_process_time}ms rid={request_id}"
    )

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
    tools = await bl_tools(["blaxel-search"])
    logger.info(f"Loaded tools in {round(time.time() - start, 4)} seconds")

    start = time.time()
    model = await bl_model("gpt-4o-mini")
    logger.info(f"Retrieved model in {round(time.time() - start, 4)} seconds")

    # CrewAI specific implementation would go here
    # This is a placeholder for the actual CrewAI agent implementation
    agent = Agent(
        role="Weather Researcher",
        goal="Find the weather in a specific city",
        backstory="You are an experienced weather researcher with attention to detail",
        llm=model,
        tools=tools,
        verbose=True,
    )
    with SpanManager("blaxel-crewai").create_active_span("agent-request", {}) as span:
        body = await request.json()
        # Placeholder response - replace with actual CrewAI implementation
        crew = Crew(
            agents=[agent],
            tasks=[
                Task(
                    description=body.get("description", "Find the weather in a specific city"),
                    expected_output=body.get("expected_output", "Weather in San francisco."),
                    agent=agent,
                )
            ],
            verbose=True,
        )
        result = crew.kickoff()
        result = f"CrewAI processed: {body.get('inputs', '')}"
        span.set_attribute("agent.result", result)
        return Response(result, media_type="text/plain")


FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")
