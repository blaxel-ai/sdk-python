
import nest_asyncio

nest_asyncio.apply()

import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def test_mcp_tools_langchain():
    tools = await bl_tools(["blaxel-search"]).to_langchain()
    if len(tools) == 0:
        raise Exception("No tools found")
    result = await tools[0].ainvoke({ "query": "What is the capital of France?"})
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

async def main():
    await test_mcp_tools_langchain()
    await test_mcp_tools_llamaindex()
    await test_mcp_tools_crewai()

if __name__ == "__main__":
    asyncio.run(main())