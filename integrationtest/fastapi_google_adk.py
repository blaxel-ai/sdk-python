import traceback
from logging import getLogger
from time import time

from dotenv import load_dotenv
from fastapi.responses import JSONResponse

logger = getLogger(__name__)
total = time()
start = time()
load_dotenv()

from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
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
    formatted_process_time = f'{process_time:.2f}'
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
    tools = await bl_tools(["github"], timeout_enabled=False).to_google_adk()
    print(f"Loaded tools in {round(time() - start, 4)} seconds")
    start = time()
    print(f"Converted tools to google adk in {round(time() - start, 4)} seconds")
    start = time()
    model = await bl_model("gpt-4o-mini").to_google_adk()
    print(f"Retrieved model in google adk in {round(time() - start, 4)} seconds")
    start = time()


    description = "Tools agent"
    prompt = """Provide any question you have with tools result. You can launch multiple tools to have your answer
    Format the response from the tool result
"""
    APP_NAME = "blaxel_test"
    SESSION_ID = "session_1"
    USER_ID = "user_1"

    agent = Agent(model=model, name=APP_NAME, description=description, instruction=prompt, tools=tools)
    # Create the specific session where the conversation will happen
    session_service = InMemorySessionService()
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    print(f"Create agent in {round(time() - start, 4)} seconds")
    with SpanManager("blaxel-langchain").create_active_span("agent-request", {}) as span:
        body = await request.json()
        input = body.get("inputs", "")
        content = types.Content(role="user", parts=[types.Part(text=input)])
        final_response_text = ""
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
        span.set_attribute("agent.result", final_response_text)
        print(final_response_text)
        return Response(
            final_response_text,
            media_type="text/plain"
        )

start = time()
FastAPIInstrumentor.instrument_app(app)
logger.info(f"Instrumented app in {round(time() - start, 4)} seconds")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")