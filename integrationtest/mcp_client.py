import os
from logging import getLogger

logger = getLogger(__name__)

os.environ["BL_FUNCTION_ADD_URL"] = "http://localhost:8080"

from blaxel.tools import bl_tools


async def main():
    async with bl_tools(["add"]) as t:
        tools = t.to_langchain()
        result = await tools[0].ainvoke({"a": 1, "b": 2})
        logger.info(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
