"""Google ADK Model Integration Tests."""

import logging
import re

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

BLOCKED_PROVIDER_LOG_PATTERNS = {
    "x_blaxel_authorization": re.compile(r"x-blaxel-authorization", re.IGNORECASE),
    "bearer": re.compile(r"\bbearer\b", re.IGNORECASE),
    "jwt_like": re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\."),
    "request_options": re.compile(r"Request options"),
    "llm_request": re.compile(r"LLM Request"),
    "raw_response": re.compile(r"RAW RESPONSE"),
}


def blocked_provider_log_counts(text: str) -> dict[str, int]:
    return {
        name: len(pattern.findall(text)) for name, pattern in BLOCKED_PROVIDER_LOG_PATTERNS.items()
    }


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

    @pytest.mark.parametrize("model_name", TEST_MODELS)
    async def test_provider_debug_logs_are_suppressed(
        self,
        model_name: str,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path,
        capsys: pytest.CaptureFixture[str],
    ):
        """Force root DEBUG and verify provider internals stay out of captured logs."""
        monkeypatch.delenv("BL_ALLOW_PROVIDER_DEBUG_LOGS", raising=False)
        root_logger = logging.getLogger()
        original_root_level = root_logger.level
        log_path = tmp_path / "provider-debug.log"
        capture_handler = logging.FileHandler(log_path)
        capture_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(capture_handler)
        root_logger.setLevel(logging.DEBUG)

        try:
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
        finally:
            root_logger.removeHandler(capture_handler)
            capture_handler.close()
            root_logger.setLevel(original_root_level)

        captured = capsys.readouterr()
        log_text = log_path.read_text()
        log_path.unlink(missing_ok=True)
        counts = blocked_provider_log_counts(f"{log_text}\n{captured.out}\n{captured.err}")

        assert len(collected_text) > 0
        assert not any(counts.values()), f"blocked provider debug logs emitted: {counts}"
