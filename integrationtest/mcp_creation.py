import logging
import os
import time

from blaxel.client import client
from blaxel.client.api.functions import create_function, delete_function, get_function
from blaxel.client.api.integrations import (
    create_integration_connection,
    delete_integration_connection,
)
from blaxel.client.models import (
    Function,
    FunctionSpec,
    IntegrationConnection,
    IntegrationConnectionSpec,
    Metadata,
    Runtime,
)
from blaxel.tools import bl_tools

logger = logging.getLogger(__name__)

async def wait_mcp_ready(name, max_wait: int = 60000, interval: int = 1000):
    start_time = time.time() * 1000
    mcp: Function = await get_function.asyncio(
        name,
        client=client,
    )
    while mcp.status != "DEPLOYED":
        await asyncio.sleep(1)
        logger.info(f"Waiting for MCP to be deployed, status: {mcp.status}")
        mcp = await get_function.asyncio(
            name,
            client=client,
        )
        if (time.time() * 1000) - start_time > max_wait:
            raise Exception("MCP did not deploy in time")

async def main():
    try:
        team_id = os.getenv("SLACK_TEAM_ID")
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        mcp_name = "my-slack-mcp"
        integration_connection_name = "my-slack-integration"

        if not team_id or not bot_token:
            raise Exception("SLACK_TEAM_ID and SLACK_BOT_TOKEN must be set")

        # Create integration connection
        integration_connection: IntegrationConnection = await create_integration_connection.asyncio(
            client=client,
            body=IntegrationConnection(
                metadata=Metadata(
                    name=integration_connection_name
                ),
                spec=IntegrationConnectionSpec(
                    integration="slack",
                    config={
                        "teamId": team_id
                    },
                    secret={
                        "botToken": bot_token
                    }
                )
            )
        )

        # Create MCP
        await create_function.asyncio(
            client=client,
            body=Function(
                metadata=Metadata(
                    name=mcp_name
                ),
                spec=FunctionSpec(
                    integration_connections=[integration_connection.metadata.name],
                    runtime=Runtime(
                        type_="mcp"
                    )
                )
            )
        )
        await wait_mcp_ready(mcp_name)

        ### DO SOME STUFF WITH MCP
        tools = await bl_tools([mcp_name]).initialize()
        print(await tools.get_tools()[0].coroutine())
    except Exception as e:
        logger.error(f"There was an error while creating/using MCP, {e}")
    finally:
        ### CLEANUP
        await delete_function.asyncio(
            mcp_name,
            client=client,
        )
        await delete_integration_connection.asyncio(
            integration_connection_name,
            client=client,
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
