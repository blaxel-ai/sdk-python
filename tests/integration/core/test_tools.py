"""Core blTools Integration Tests."""

import asyncio

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.tools import bl_tools as bl_tools_core
from tests.helpers import default_image, default_labels, unique_name


class TestCoreBlToolsSync:
    """Test core blTools sync functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest.fixture(autouse=True, scope="class")
    def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("core-sync-tools-test")

        async def create_sandbox():
            return await SandboxInstance.create(
                {
                    "name": request.cls.sandbox_name,
                    "image": default_image,
                    "memory": 2048,
                    "labels": default_labels,
                }
            )

        request.cls.sandbox = asyncio.get_event_loop().run_until_complete(create_sandbox())

        yield

        # Cleanup
        async def cleanup():
            try:
                await request.cls.sandbox.delete()
            except Exception:
                pass

        try:
            asyncio.get_event_loop().run_until_complete(cleanup())
        except Exception:
            pass

    def test_can_get_tool_names(self):
        """Test getting tool names."""
        tools = bl_tools_core([f"sandbox/{self.sandbox_name}"])

        assert tools.functions is not None
        assert len(tools.functions) > 0


@pytest.mark.asyncio(loop_scope="class")
class TestCoreBlTools:
    """Test core blTools functionality."""

    sandbox: SandboxInstance | None = None
    sandbox_name: str | None = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("core-tools-test")
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
            await request.cls.sandbox.delete()
        except Exception:
            pass

    async def test_can_get_and_invoke_tools(self):
        """Test getting and invoking tools."""
        tools_wrapper = bl_tools_core([f"sandbox/{self.sandbox_name}"])
        await tools_wrapper.initialize()
        tools = tools_wrapper.get_tools()

        assert len(tools) > 0

        # Find the exec tool to test
        exec_tool = next((t for t in tools if "exec" in t.name.lower()), None)
        assert exec_tool is not None
        assert exec_tool.coroutine is not None
        result = await exec_tool.coroutine(
            command="echo 'hello'",
        )
        assert result is not None
