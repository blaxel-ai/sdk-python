import nest_asyncio

# This is because crewai is not asyncio compatible for now: https://github.com/crewAIInc/crewAI/issues/195
nest_asyncio.apply()

import time
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from crewai import Agent, Crew, Task
from fastapi import FastAPI, Request, Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

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

@app.post("/")
async def handle_request(request: Request):
    tools = await bl_tools(["blaxel-search"]).to_crewai()
    model = await bl_model("gpt-4o-mini").to_crewai()
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
        crew = Crew(
            agents=[agent],
            tasks=[
                Task(
                    description=body.get("description", "Find the weather in a specific city"),
                    expected_output=body.get("expected_output", "Weather in San francisco."),
                    agent=agent
                )
            ],
            verbose=True,
        )
        result = crew.kickoff()
        span.set_attribute("agent.result", result.raw)
        return Response(
            result.raw,
            media_type="text/plain"
        )

FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")
