
import nest_asyncio

nest_asyncio.apply()

import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.tools import BlTools

logger = getLogger(__name__)

async def test_mcp_tools_langchain():
    async with BlTools(["blaxel-search"]) as bl_tools:
        tools = bl_tools.to_langchain()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = await tools[0].ainvoke({ "query": "What is the capital of France?"})
        logger.info(result)

async def test_mcp_tools_llamaindex():
    async with BlTools(["blaxel-search"]) as bl_tools:
        tools = bl_tools.to_llamaindex()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = await tools[0].acall(query="What is the capital of France?")
        logger.info(result)

async def test_mcp_tools_crewai():
    async with BlTools(["blaxel-search"]) as bl_tools:
        tools = bl_tools.to_crewai()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = tools[0].run(query="What is the capital of France?")
        logger.info(result)

async def main():
    await test_mcp_tools_langchain()
    await test_mcp_tools_llamaindex()
    await test_mcp_tools_crewai()

if __name__ == "__main__":
    asyncio.run(main())