"""LiveKit Model Integration Tests."""

pytest_plugins = []
from unittest.mock import Mock, patch

import pytest  # noqa: E402

pytest.importorskip(
    "livekit.agents", reason="livekit-agents not installed (install with: blaxel[livekit])"
)

from livekit.agents.llm import ChatContext  # noqa: E402

from blaxel.livekit import bl_model  # noqa: E402
from blaxel.livekit.model import get_livekit_model  # noqa: E402

TEST_MODELS = [
    "sandbox-openai",
]


async def _created_livekit_kwargs(provider_type: str, model: str, **kwargs):
    llm = Mock(name="llm")
    http_client = Mock(name="http_client")
    openai_client = Mock(name="openai_client")

    with (
        patch("blaxel.livekit.model.DynamicHeadersHTTPClient", return_value=http_client),
        patch("blaxel.livekit.model.AsyncOpenAI", return_value=openai_client),
        patch("blaxel.livekit.model.openai.LLM", return_value=llm) as llm_factory,
    ):
        result = await get_livekit_model(
            "https://example.com/models/test", provider_type, model, **kwargs
        )

    assert result is llm
    return llm_factory.call_args.kwargs


@pytest.mark.asyncio
async def test_gpt54_openai_models_default_reasoning_effort_to_none():
    for model_name in ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"]:
        kwargs = await _created_livekit_kwargs("openai", model_name)

        assert kwargs["model"] == model_name
        assert kwargs["reasoning_effort"] == "none"


@pytest.mark.asyncio
async def test_livekit_reasoning_effort_override_is_preserved():
    kwargs = await _created_livekit_kwargs("openai", "gpt-5.4-mini", reasoning_effort="low")

    assert kwargs["reasoning_effort"] == "low"


@pytest.mark.asyncio
async def test_livekit_non_openai_provider_does_not_default_reasoning_effort():
    kwargs = await _created_livekit_kwargs("xai", "gpt-5.4-mini")

    assert "reasoning_effort" not in kwargs


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
