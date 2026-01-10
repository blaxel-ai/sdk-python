"""LlamaIndex Integration Tests."""

import pytest
import pytest_asyncio
from llama_index.core.llms import ChatMessage

from blaxel.core.sandbox import SandboxInstance
from blaxel.llamaindex import bl_model, bl_tools
from tests.helpers import default_image, default_labels, unique_name

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
        result = await model.achat([ChatMessage(role="user", content="Say hello in one word")])

        assert result is not None
        assert result.message is not None
        assert result.message.content is not None


@pytest.mark.asyncio(loop_scope="class")
class TestBlTools:
    """Test bl_tools functionality."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("llamaindex-model-test")
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

    async def test_can_load_sandbox_tools(self):
        """Test loading sandbox tools."""
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0
        assert tools[0] is not None

    async def test_can_invoke_a_tool(self):
        """Test invoking a tool."""
        tools = await bl_tools([f"sandbox/{self.sandbox_name}"])

        assert len(tools) > 0

        # Find the exec tool
        exec_tool = next((t for t in tools if "exec" in t.metadata.name.lower()), None)
        if exec_tool:
            result = await exec_tool.acall(
                command="echo 'Hello'",
            )

            assert result is not None
