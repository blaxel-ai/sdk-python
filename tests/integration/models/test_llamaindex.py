"""LlamaIndex Integration Tests."""

import pytest

from blaxel.llamaindex import bl_model, bl_tools
from llama_index.core.llms import ChatMessage


TEST_MODELS = [
    "sandbox-openai",
]

@pytest.mark.asyncio(loop_scope="class")
class TestBlModel:
    """Test bl_model functionality."""

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_chat_with_model(self, model_name: str):
        """Test chatting with a model."""
        model = await bl_model(model_name)
        result = await model.achat([
            ChatMessage(role="user", content="Say hello in one word")
        ])

        assert result is not None
        assert result.message is not None
        assert result.message.content is not None


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    async def test_can_load_mcp_tools(self):
        """Test loading MCP tools."""
        tools = await bl_tools(["blaxel-search"])

        assert len(tools) > 0
        assert tools[0] is not None

    async def test_can_invoke_a_tool(self):
        """Test invoking a tool."""
        tools = await bl_tools(["blaxel-search"])

        assert len(tools) > 0

        result = await tools[0].acall(
            query="What is the capital of France?",
        )

        assert result is not None
