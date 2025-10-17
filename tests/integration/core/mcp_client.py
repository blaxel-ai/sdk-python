import asyncio

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from blaxel import settings


async def run():
    """Run the completion client example."""
    url = f"{settings.run_url}/{settings.workspace}/functions/blaxel-search/mcp"

    async with streamablehttp_client(url, settings.headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            tools = await session.list_tools()
            print(f"Tools retrieved, number of tools: {len(tools.tools)}")

asyncio.run(run())