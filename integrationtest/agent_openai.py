import asyncio

from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

# Only compatible with openai models
MODEL = "gpt-4o-mini"

async def main():
    tools = await bl_tools(["blaxel-search"]).to_openai()
    model = await bl_model(MODEL).to_openai()

    agent = Agent(
        name="blaxel-agent",
        model=model,
        tools=tools,
        instructions="You are a helpful assistant. Maximum number of tool call is 1",
    )
    input = "Search online for the current weather in San Francisco ?"
    # input = "What are the tools in your arsenal ?"
    # input = "Hello world"
    result = await Runner.run(agent, input)
    logger.info(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())