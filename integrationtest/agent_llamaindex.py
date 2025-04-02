import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from llama_index.core.agent.workflow import ReActAgent, ToolCallResult
from llama_index.core.workflow import Context

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

MODEL = "gpt-4o-mini"
# MODEL = "xai-grok-beta"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"
# MODEL = "claude-3-5-sonnet"
# MODEL = "cohere-command-r-plus" # x -> Error in step 'run_agent_step': 'async for' requires an object with __aiter__ method, got generator
# MODEL = "gemini-2-0-flash"

async def main():
    tools = await bl_tools(["blaxel-search"]).to_llamaindex()
    model = await bl_model(MODEL).to_llamaindex()

    agent = ReActAgent(llm=model, tools=tools, system_prompt="You are a helpful assistant. Maximum number of tool call is 1.")
    context = Context(agent)
    input = "Search online for the current weather in San Francisco ?"
    # input = "What are the tools in your arsenal ?"
    # input = "Hello world"
    handler = agent.run(input, ctx=context)
    async for ev in handler.stream_events():
        if isinstance(ev, ToolCallResult):
            logger.info(f"Call {ev.tool_name} with {ev.tool_kwargs}")
    response = await handler
    logger.info(response)

if __name__ == "__main__":
    asyncio.run(main())