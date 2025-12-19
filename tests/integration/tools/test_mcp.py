"""MCP Client Integration Tests.

Note: These tests require special authentication setup for raw MCP SDK.
The blTools wrapper in test_bltools.py handles auth automatically.
"""

import pytest

from blaxel.core import settings
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@pytest.mark.asyncio(loop_scope="class")
class TestMCPClientIntegration:
    """Test MCP client integration."""

    async def test_streamable_http_transport(self):
        """Test Streamable HTTP Transport."""
        base_url = f"{settings.run_url}/{settings.workspace}/functions/blaxel-search/mcp"

        async with streamablehttp_client(
            base_url,
            headers=settings.headers,
        ) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # Verify connection worked
                assert session is not None

                response = await session.list_tools()

                assert response is not None
