import nest_asyncio

nest_asyncio.apply()

import asyncio

from dotenv import load_dotenv
from pydantic_ai import Agent, CallToolsNode
from pydantic_ai.messages import ToolCallPart

load_dotenv()

from logging import getLogger

from blaxel.core.tools import bl_tools

logger = getLogger(__name__)


async def test_mcp_tools_langchain():
    """Test bl_tools to_langchain conversion."""
    print("Testing LangChain tools conversion...")
    tools = await bl_tools(["blaxel-search"]).to_langchain()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].ainvoke({"query": "What is the capital of France?"})
    result = await tools[0].ainvoke({"query": "What is the capital of USA?"})
    logger.info(f"LangChain tools result: {result}")
    print(f"LangChain tools result: {result}")


async def test_mcp_tools_llamaindex():
    """Test bl_tools to_llamaindex conversion."""
    print("Testing LlamaIndex tools conversion...")
    tools = await bl_tools(["blaxel-search"]).to_llamaindex()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].acall(query="What is the capital of France?")
    logger.info(f"LlamaIndex tools result: {result}")
    print(f"LlamaIndex tools result: {result}")


async def test_mcp_tools_crewai():
    """Test bl_tools to_crewai conversion."""
    print("Testing CrewAI tools conversion...")
    tools = await bl_tools(["blaxel-search"]).to_crewai()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = tools[0].run(query="What is the capital of France?")
    logger.info(f"CrewAI tools result: {result}")
    print(f"CrewAI tools result: {result}")


async def test_mcp_tools_pydantic():
    """Test bl_tools to_pydantic conversion."""
    print("Testing Pydantic tools conversion...")
    tools = await bl_tools(["blaxel-search"]).to_pydantic()
    if len(tools) == 0:
        raise Exception("No tools found")

    agent = Agent(model="openai:gpt-4o-mini", tools=tools)
    async with agent.iter("Search what is the capital of France?") as agent_run:
        async for node in agent_run:
            # Each node represents a step in the agent's execution
            if isinstance(node, CallToolsNode):
                for part in node.model_response.parts:
                    if isinstance(part, ToolCallPart):
                        logger.info(f"Tool call: {part}")
                        print(f"Tool call: {part}")
                    else:
                        logger.info(f"Response: {part}")
                        print(f"Response: {part}")


async def test_mcp_tools_google_adk():
    """Test bl_tools to_google_adk conversion."""
    print("Testing Google ADK tools conversion...")
    tools = await bl_tools(["blaxel-search"]).to_google_adk()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].run_async(
        args={"query": "What is the capital of France?"}, tool_context=None
    )
    logger.info(f"Google ADK tools result: {result}")
    print(f"Google ADK tools result: {result}")


async def test_mcp_tools_blaxel():
    """Test bl_tools native blaxel functionality."""
    print("Testing native Blaxel tools...")
    tools = bl_tools(["blaxel-search"], {"test": "test"})
    await tools.intialize()
    blaxel_tools = tools.get_tools()
    if len(blaxel_tools) == 0:
        raise Exception("No tools found")
    result = await blaxel_tools[0].coroutine(query="What is the capital of France?")
    logger.info(f"Blaxel tools result: {result}")
    print(f"Blaxel tools result: {result}")
    result = await blaxel_tools[0].coroutine(query="What is the capital of Germany?")
    logger.info(f"Blaxel tools result: {result}")
    print(f"Blaxel tools result: {result}")
    await asyncio.sleep(7)
    result = await blaxel_tools[0].coroutine(query="What is the capital of USA?")
    logger.info(f"Blaxel tools result: {result}")
    print(f"Blaxel tools result: {result}")
    result = await blaxel_tools[0].coroutine(query="What is the capital of Canada?")
    logger.info(f"Blaxel tools result: {result}")
    print(f"Blaxel tools result: {result}")


async def main():
    """Main function for standalone execution."""
    await test_mcp_tools_blaxel()
    await test_mcp_tools_langchain()
    await test_mcp_tools_llamaindex()
    await test_mcp_tools_crewai()
    await test_mcp_tools_pydantic()
    await test_mcp_tools_google_adk()


if __name__ == "__main__":
    asyncio.run(main())
