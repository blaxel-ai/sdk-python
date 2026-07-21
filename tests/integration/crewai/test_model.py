"""CrewAI Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip("crewai", reason="crewai not installed (install with: blaxel[crewai])")


from blaxel.crewai import bl_model  # noqa: E402

TEST_MODELS = [
    "sandbox-openai",
]


def _is_live_model_gateway_error(exc: Exception) -> bool:
    text = f"{type(exc).__module__}.{type(exc).__name__}: {exc}".lower()
    return any(
        fragment in text
        for fragment in (
            "authentication error: invalid token",
            "unsupported value",
            "rate limit",
            "timeout",
            "connection error",
            "service unavailable",
            "internal server error",
            "bad gateway",
            "gateway timeout",
        )
    )


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
        try:
            result = model.call(messages=[{"role": "user", "content": "Say hello in one word"}])
        except Exception as e:
            if not _is_live_model_gateway_error(e):
                raise
            # This exercises the live model gateway through crewai/litellm. Skip on
            # environment issues (gateway auth rejection, model param incompatibility)
            # instead of failing CI on infrastructure unrelated to the SDK call path.
            pytest.skip(f"crewai model call unavailable in this environment: {e}")

        assert result is not None
