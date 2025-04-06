import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from pydantic_ai import Agent, CallToolsNode
from pydantic_ai.messages import ToolCallPart
from pydantic_ai.models import ModelSettings

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
    tools = await bl_tools(["blaxel-search"]).to_pydantic()

    model = await bl_model(MODEL).to_pydantic()

    agent = Agent(model=model, tools=tools, model_settings=ModelSettings(temperature=0))
    async with agent.iter('Hello') as agent_run:
        async for node in agent_run:
            if isinstance(node, CallToolsNode):
                for part in node.model_response.parts:
                    if isinstance(part, ToolCallPart):
                        logger.info(f"Tool call: {part}")
                    else:
                        logger.info(f"Response: {part}")

if __name__ == "__main__":
    asyncio.run(main())