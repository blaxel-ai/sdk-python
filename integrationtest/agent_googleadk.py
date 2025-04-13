import asyncio

from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

load_dotenv()

from logging import getLogger

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

# MODEL = "gpt-4o-mini"
# MODEL = "claude-3-5-sonnet"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus" # x -> tool call not supported
MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"

async def main():
    # Define constants for identifying the interaction context
    APP_NAME = "weather_agent"
    USER_ID = "user_1"
    SESSION_ID = "session_001" # Using a fixed ID for simplicity

    tools = await bl_tools(["blaxel-search"], timeout_enabled=False).to_google_adk()
    model = await bl_model(MODEL, temperature=0).to_google_adk()

    description = "Provides weather information for specific cities."
    prompt = """You are a helpful weather assistant. Your primary goal is to provide current weather reports. "
When the user asks for the weather in a specific city,
Analyze the tool's response: if the status is 'error', inform the user politely about the error message.
If the status is 'success', present the weather 'report' clearly and concisely to the user.
Only use the tool when a city is mentioned for a weather request.
"""
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
    print(f"Runner created for agent '{runner.agent.name}'.")

    input = "What is the weather like in London?"
    content = types.Content(role="user", parts=[types.Part(text=input)])
    final_response_text = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
        if event.content and event.content.parts:
            # Assuming text response in the first part
            final_response_text = event.content.parts[0].text
        elif event.actions and event.actions.escalate: # Handle potential errors/escalations
            final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"

        # Add more checks here if needed (e.g., specific error codes)
        break # Stop processing events once the final response is found
    print(f"Final response: {final_response_text}")

if __name__ == "__main__":
    asyncio.run(main())