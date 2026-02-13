"""Google ADK Model Integration Tests."""

pytest_plugins = []
import pytest  # noqa: E402

pytest.importorskip(
    "google.adk", reason="google-adk not installed (install with: blaxel[googleadk])"
)

from google.adk.models import LlmRequest  # noqa: E402
from google.genai import types  # noqa: E402

from blaxel.googleadk import bl_model  # noqa: E402

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

        request = LlmRequest(
            contents=[
                types.Content(
                    parts=[types.Part(text="Say hello in one word")],
                    role="user",
                )
            ],
            config=types.GenerateContentConfig(),
        )

        collected_text = ""
        async for response in model.generate_content_async(request):
            assert response is not None
            if response.content and response.content.parts:
                for part in response.content.parts:
                    if part.text:
                        collected_text += part.text

        assert len(collected_text) > 0
