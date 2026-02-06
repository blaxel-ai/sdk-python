"""LlamaIndex Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("llama_index", reason="llama-index not installed (install with: blaxel[llamaindex])")

from llama_index.core.base.llms.base import BaseLLM  # type: ignore[import-not-found]
from llama_index.core.llms import ChatMessage  # type: ignore[import-not-found]
from llama_index.core.llms.function_calling import (  # type: ignore[import-not-found]
    FunctionCallingLLM,
)

from blaxel.llamaindex import bl_model  # noqa: E402

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