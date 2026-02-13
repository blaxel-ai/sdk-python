"""Pydantic AI Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip(
    "pydantic_ai", reason="pydantic-ai not installed (install with: blaxel[pydantic])"
)

from pydantic_ai import Agent  # noqa: E402

from blaxel.pydantic import bl_model  # noqa: E402

TEST_MODELS = [
    "sandbox-openai",
]


@pytest.mark.asyncio(loop_scope="class")
class TestBlModel:
    """Test bl_model functionality."""

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_create_model(self, model_name: str):
        """Test creating a model."""
        model = await bl_model(model_name)

        assert model is not None

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_run_agent(self, model_name: str):
        """Test running an agent with the model."""
        model = await bl_model(model_name)
        agent = Agent(model=model, system_prompt="Say hello in one word")
        result = await agent.run("Say hello")

        assert result is not None
        assert result.output is not None
