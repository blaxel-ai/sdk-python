"""LiveKit Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip(
    "livekit.agents", reason="livekit-agents not installed (install with: blaxel[livekit])"
)

from livekit.agents.llm import ChatContext  # noqa: E402

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

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_can_call_model(self, model_name: str):
        """Test making an actual request to the model."""
        model = await bl_model(model_name)

        chat_ctx = ChatContext.empty()
        chat_ctx.add_message(role="user", content="Say hello in one word")

        stream = model.chat(chat_ctx=chat_ctx)

        collected_text = ""
        async for chunk in stream:
            if chunk.delta and chunk.delta.content:
                collected_text += chunk.delta.content

        assert len(collected_text) > 0
