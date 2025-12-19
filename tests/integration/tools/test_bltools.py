"""MCP Tools Integration Tests."""

import pytest
from blaxel.langgraph import bl_tools as bl_tools_langgraph
from blaxel.llamaindex import bl_tools as bl_tools_llamaindex
from blaxel.openai import bl_tools as bl_tools_openai


from blaxel.core.tools import bl_tools as bl_tools_core


@pytest.mark.asyncio(loop_scope="class")
class TestLanggraphTools:
    """Test LangGraph tools."""

    async def test_can_load_tools_from_blaxel_search(self):
        """Test loading tools from blaxel-search."""
        tools = await bl_tools_langgraph(["blaxel-search"])

        assert len(tools) > 0

    async def test_can_invoke_a_tool(self):
        """Test invoking a tool."""
        tools = await bl_tools_langgraph(["blaxel-search"])

        assert len(tools) > 0

        result = await tools[0].ainvoke({
            "query": "What is the capital of France?",
        })

        assert result is not None


@pytest.mark.asyncio(loop_scope="class")
class TestLlamaindexTools:
    """Test LlamaIndex tools."""

    async def test_can_load_tools_from_blaxel_search(self):
        """Test loading tools from blaxel-search."""
        tools = await bl_tools_llamaindex(["blaxel-search"])

        assert len(tools) > 0

    async def test_can_call_a_tool(self):
        """Test calling a tool."""
        tools = await bl_tools_llamaindex(["blaxel-search"])

        assert len(tools) > 0

        result = await tools[0].acall(
            query="What is the capital of France?",
        )

        assert result is not None


@pytest.mark.asyncio(loop_scope="class")
class TestOpenAITools:
    """Test OpenAI tools."""

    async def test_can_load_tools_from_blaxel_search(self):
        """Test loading tools from blaxel-search."""
        tools = await bl_tools_openai(["blaxel-search"])

        assert tools is not None
        assert len(tools) > 0


class TestCoreBlToolsSync:
    """Test core blTools sync functionality."""

    def test_can_get_tool_names(self):
        """Test getting tool names."""
        tools = bl_tools_core(["blaxel-search"])

        assert tools.functions is not None
        assert len(tools.functions) > 0


@pytest.mark.asyncio(loop_scope="class")
class TestCoreBlTools:
    """Test core blTools functionality."""

    async def test_can_get_and_invoke_tools(self):
        """Test getting and invoking tools."""
        tools_wrapper = bl_tools_core(["blaxel-search"])
        await tools_wrapper.initialize()
        tools = tools_wrapper.get_tools()

        assert len(tools) > 0

        result = await tools[0].coroutine(
            query="What is the capital of France?",
        )

        assert result is not None

