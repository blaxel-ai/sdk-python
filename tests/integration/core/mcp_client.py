import asyncio
import os
from logging import getLogger

logger = getLogger(__name__)

os.environ["BL_FUNCTION_ADD_URL"] = "http://localhost:8080"

from blaxel.langgraph.tools import bl_tools


async def main():
    """Main function for standalone execution."""
    print("Testing MCP client functionality...")

    # Get langchain tools directly
    tools = await bl_tools(["add"])
    if len(tools) == 0:
        raise Exception("No tools found")

    # Test the tool
    result = await tools[0].ainvoke({"a": 1, "b": 2})
    logger.info(f"MCP client result: {result}")
    print(f"MCP client result: {result}")

    print("✅ MCP client test completed!")


if __name__ == "__main__":
    asyncio.run(main())
