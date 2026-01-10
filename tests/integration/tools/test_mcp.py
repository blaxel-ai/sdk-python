"""MCP Client Integration Tests.

Note: These tests require special authentication setup for raw MCP SDK.
The blTools wrapper in test_bltools.py handles auth automatically.
"""

import pytest
import pytest_asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from blaxel.core import settings
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestMCPClientIntegration:
    """Test MCP client integration."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("mcp-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass

    async def test_streamable_http_transport(self):
        """Test Streamable HTTP Transport."""
        base_url = f"{self.sandbox.metadata.url}/mcp"

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
