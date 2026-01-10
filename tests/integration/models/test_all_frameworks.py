"""All Frameworks Model Compatibility Tests.

This test suite verifies that all model frameworks work with the same set of models.
It tests basic functionality across langgraph, llamaindex, openai, and pydantic integrations.
"""

import pytest

from blaxel.langgraph import bl_model as bl_model_langgraph
from blaxel.llamaindex import bl_model as bl_model_llamaindex
from blaxel.openai import bl_model as bl_model_openai
from blaxel.pydantic import bl_model as bl_model_pydantic

TEST_MODELS = [
    "sandbox-openai",
]


@pytest.mark.asyncio(loop_scope="class")
class TestAllFrameworksModelCompatibility:
    """Test model compatibility across all frameworks."""

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_works_with_langgraph(self, model_name: str):
        """Test model works with LangGraph."""
        model = await bl_model_langgraph(model_name)
        assert model is not None

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_works_with_llamaindex(self, model_name: str):
        """Test model works with LlamaIndex."""
        model = await bl_model_llamaindex(model_name)
        assert model is not None

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_works_with_openai(self, model_name: str):
        """Test model works with OpenAI Agents SDK.

        Note: This test requires a model that has type 'openai' configured.
        OpenAIChatCompletionsModel is designed for use with the agents framework,
        so we just verify it was created correctly.
        """
        model = await bl_model_openai(model_name)
        assert model is not None

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_works_with_pydantic(self, model_name: str):
        """Test model works with Pydantic AI."""
        model = await bl_model_pydantic(model_name)

        assert model is not None
