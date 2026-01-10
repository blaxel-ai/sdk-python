"""MCP Tools Integration Tests."""

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.tools import bl_tools as bl_tools_core
from blaxel.langgraph import bl_tools as bl_tools_langgraph
from blaxel.llamaindex import bl_tools as bl_tools_llamaindex
from blaxel.openai import bl_tools as bl_tools_openai
from tests.helpers import default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestLanggraphTools:
    """Test LangGraph tools."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("langgraph-tools-test")
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

    async def test_can_load_tools_from_sandbox(self):
        """Test loading tools from sandbox."""
        tools = await bl_tools_langgraph([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

    async def test_can_invoke_a_tool(self):
        """Test invoking a tool."""
        tools = await bl_tools_langgraph([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

        # Find the exec tool to test
        exec_tool = next((t for t in tools if "exec" in t.name.lower()), None)
        if exec_tool:
            result = await exec_tool.ainvoke(
                {
                    "command": "echo 'hello'",
                }
            )
            assert result is not None


@pytest.mark.asyncio(loop_scope="class")
class TestLlamaindexTools:
    """Test LlamaIndex tools."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("llamaindex-tools-test")
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

    async def test_can_load_tools_from_sandbox(self):
        """Test loading tools from sandbox."""
        tools = await bl_tools_llamaindex([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

    async def test_can_call_a_tool(self):
        """Test calling a tool."""
        tools = await bl_tools_llamaindex([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

        # Find the exec tool to test
        exec_tool = next((t for t in tools if "exec" in t.metadata.name.lower()), None)
        if exec_tool:
            result = await exec_tool.acall(
                command="echo 'hello'",
            )
            assert result is not None


@pytest.mark.asyncio(loop_scope="class")
class TestOpenAITools:
    """Test OpenAI tools."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("openai-tools-test")
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

    async def test_can_load_tools_from_sandbox(self):
        """Test loading tools from sandbox."""
        tools = await bl_tools_openai([f"sandbox/{self.sandbox_name}"])

        assert tools is not None
        assert len(tools) > 0


class TestCoreBlToolsSync:
    """Test core blTools sync functionality."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest.fixture(autouse=True, scope="class")
    def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        import asyncio

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
                await SandboxInstance.delete(request.cls.sandbox_name)
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

    sandbox: SandboxInstance = None
    sandbox_name: str = None

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
            await SandboxInstance.delete(request.cls.sandbox_name)
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
        if exec_tool:
            result = await exec_tool.coroutine(
                command="echo 'hello'",
            )
            assert result is not None
