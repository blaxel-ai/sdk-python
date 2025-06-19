import asyncio
import os
from logging import getLogger

logger = getLogger(__name__)

os.environ["BL_FUNCTION_ADD_URL"] = "http://localhost:8080"

from blaxel.core.tools import bl_tools


async def main():
    """Main function for standalone execution."""
    print("Testing MCP client functionality...")
    async with bl_tools(["add"]) as t:
        tools = t.to_langchain()
        if len(tools) == 0:
            raise Exception("No tools found")
        result = await tools[0].ainvoke({"a": 1, "b": 2})
        logger.info(f"MCP client result: {result}")
        print(f"MCP client result: {result}")
    print("✅ MCP client test completed!")


if __name__ == "__main__":
    asyncio.run(main())
