import asyncio
import os

from dotenv import load_dotenv

load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"

from logging import getLogger

from blaxel.tools import BlaxelTools

logger = getLogger(__name__)

async def test_mcp_tools_langchain():
    async with BlaxelTools(["blaxel-search"]) as blaxel_tools:
        tools = blaxel_tools.to_langchain()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = await tools[0].ainvoke({ "query": "What is the capital of France?"})
        logger.info(result)

async def test_mcp_tools_llamaindex():
    async with BlaxelTools(["blaxel-search"]) as blaxel_tools:
        tools = blaxel_tools.to_llamaindex()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = await tools[0].acall(query="What is the capital of France?")
        logger.info(result)

async def main():
    # await test_mcp_tools_langchain()
    await test_mcp_tools_llamaindex()

if __name__ == "__main__":
    asyncio.run(main())