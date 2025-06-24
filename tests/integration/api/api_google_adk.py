# ruff: noqa: E402

import dotenv

dotenv.load_dotenv()

# Disable litellm logger
import traceback
from contextlib import asynccontextmanager
from logging import getLogger
from time import time

import litellm
import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from blaxel.googleadk import bl_model, bl_tools

litellm._logging._disable_debugging()

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server running on port 1338")
    yield
    logger.info("Server shutting down")


MODEL = "gpt-4o-mini"
# MODEL = "claude-3-7-sonnet-20250219"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus" # x -> tool call not supported
# MODEL = "gemini-2-5-pro-preview-03-25"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    response: Response = await call_next(request)

    process_time = (time() - start_time) * 1000
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


async def weather(city: str) -> str:
    """Get the weather in a given city"""
    return f"The weather in {city} is sunny"


@app.post("/")
async def handle_request(request: Request):
    APP_NAME = "weather_agent"
    USER_ID = "user_1"
    SESSION_ID = "session_001"  # Using a fixed ID for simplicity

    tools = await bl_tools(["blaxel-search"], timeout_enabled=False)
    model = await bl_model(MODEL, temperature=0)

    description = "Provides weather information for specific cities."
    prompt = """You are a helpful weather assistant. Your primary goal is to provide current weather reports. "
When the user asks for the weather in a specific city,
Analyze the tool's response: if the status is 'error', inform the user politely about the error message.
If the status is 'success', present the weather 'report' clearly and concisely to the user.
Only use the tool when a city is mentioned for a weather request.
"""
    agent = Agent(
        model=model, name=APP_NAME, description=description, instruction=prompt, tools=tools
    )

    # Create the specific session where the conversation will happen
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    logger.info(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    logger.info(f"Runner created for agent '{runner.agent.name}'.")

    input = "What is the weather like in London?"
    content = types.Content(role="user", parts=[types.Part(text=input)])
    final_response_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )

            # Add more checks here if needed (e.g., specific error codes)
            break  # Stop processing events once the final response is found
    return Response(final_response_text, media_type="text/plain")


FastAPIInstrumentor.instrument_app(app, exclude_spans=["receive", "send"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1338, log_level="critical", loop="asyncio")
