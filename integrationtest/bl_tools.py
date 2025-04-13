import nest_asyncio

nest_asyncio.apply()

import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent, CallToolsNode
from pydantic_ai.messages import ToolCallPart

load_dotenv()

from logging import getLogger

from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def test_mcp_tools_langchain():
    tools = await bl_tools(["blaxel-search"]).to_langchain()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].ainvoke({ "query": "What is the capital of France?"})
    result = await tools[0].ainvoke({ "query": "What is the capital of USA?"})
    logger.info(result)

async def test_mcp_tools_llamaindex():
    tools = await bl_tools(["blaxel-search"]).to_llamaindex()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].acall(query="What is the capital of France?")
    logger.info(result)

async def test_mcp_tools_crewai():
    tools = await bl_tools(["blaxel-search"]).to_crewai()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = tools[0].run(query="What is the capital of France?")
    logger.info(result)

async def test_mcp_tools_pydantic():
    tools = await bl_tools(["blaxel-search"]).to_pydantic()
    if len(tools) == 0:
        raise Exception("No tools found")

    agent = Agent(model='openai:gpt-4o-mini', tools=tools)
    # result = await agent.run('What is the capital of France?', deps='human')
    async with agent.iter('Search what is the capital of France?') as agent_run:
        async for node in agent_run:
            # Each node represents a step in the agent's execution
            if isinstance(node, CallToolsNode):
                for part in node.model_response.parts:
                    if isinstance(part, ToolCallPart):
                        logger.info(f"Tool call: {part}")
                    else:
                        logger.info(f"Response: {part}")

async def test_mcp_tools_google_adk():
    tools = await bl_tools(["blaxel-search"]).to_google_adk()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].run_async(args={"query": "What is the capital of France?"}, tool_context=None)
    logger.info(result)

async def test_mcp_tools_blaxel():
    tools = bl_tools(["blaxel-search"], {"test": "test"})
    await tools.intialize()
    blaxel_tools = tools.get_tools()
    if len(blaxel_tools) == 0:
        raise Exception("No tools found")
    result = await blaxel_tools[0].coroutine(query="What is the capital of France?")
    logger.info(result)
    result = await blaxel_tools[0].coroutine(query="What is the capital of Germany?")
    logger.info(result)
    await asyncio.sleep(7)
    result = await blaxel_tools[0].coroutine(query="What is the capital of USA?")
    logger.info(result)
    result = await blaxel_tools[0].coroutine(query="What is the capital of Canada?")
    logger.info(result)

async def main():
    await test_mcp_tools_blaxel()
    await test_mcp_tools_langchain()
    await test_mcp_tools_llamaindex()
    await test_mcp_tools_crewai()
    await test_mcp_tools_pydantic()
    await test_mcp_tools_google_adk()

if __name__ == "__main__":
    asyncio.run(main())