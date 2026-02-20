"""LangGraph Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("langgraph", reason="langgraph not installed (install with: blaxel[langgraph])")

from blaxel.langgraph import bl_model  # noqa: E402

TEST_MODELS = [
    "sandbox-openai",
]


@pytest.mark.asyncio(loop_scope="class")
class TestBlModel:
    """Test bl_model functionality."""

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_invoke_model(self, model_name: str):
        """Test invoking a model."""
        model = await bl_model(model_name)
        result = await model.ainvoke("Say hello in one word")

        assert result is not None
        assert result.content is not None
        assert isinstance(result.content, str)
