"""LiveKit Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("livekit.agents", reason="livekit-agents not installed (install with: blaxel[livekit])")

from blaxel.livekit import bl_model  # noqa: E402

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
