"""CrewAI Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("crewai", reason="crewai not installed (install with: blaxel[crewai])")


from blaxel.crewai import bl_model  # noqa: E402

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
    async def test_can_call_model(self, model_name: str):
        """Test calling a model."""
        model = await bl_model(model_name)
        result = model.call(messages=[{"role": "user", "content": "Say hello in one word"}])

        assert result is not None
