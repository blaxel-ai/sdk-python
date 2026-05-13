from logging import getLogger

import httpx
from livekit.plugins import openai  # type: ignore[import-not-found]
from openai import AsyncOpenAI  # type: ignore[import-not-found]

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)

GPT_54_REASONING_MODELS = {"gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"}


def _provider_type_value(provider_type):
    return getattr(provider_type, "value", provider_type)


def _set_default_reasoning_effort(provider_type, model: str, kwargs: dict):
    if (
        _provider_type_value(provider_type) == "openai"
        and model in GPT_54_REASONING_MODELS
        and "reasoning_effort" not in kwargs
    ):
        kwargs["reasoning_effort"] = "none"


class DynamicHeadersHTTPClient(httpx.AsyncClient):
    """Custom HTTP client that dynamically updates headers on each request."""

    def __init__(self, base_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    async def send(self, request, *args, **kwargs):
        # Update headers with the latest auth headers before each request
        auth_headers = settings.auth.get_headers()
        # Remove the SDK's default "Authorization: Bearer replaced" header
        # when our auth uses a different header (e.g. X-Blaxel-Authorization with API keys)
        if "Authorization" not in auth_headers:
            request.headers.pop("Authorization", None)
            request.headers.pop("authorization", None)
        for key, value in auth_headers.items():
            request.headers[key] = value
        return await super().send(request, *args, **kwargs)


async def get_livekit_model(url: str, type: str, model: str, **kwargs):
    _set_default_reasoning_effort(type, model, kwargs)

    # Create custom HTTP client with dynamic headers
    http_client = AsyncOpenAI(
        base_url=f"{url}/v1",
        api_key="replaced",
        http_client=DynamicHeadersHTTPClient(
            base_url=f"{url}/v1",
        ),
    )

    if type == "xai":
        return openai.LLM(
            model=model,
            **kwargs,
            client=http_client,
        )
    else:
        if type != "openai":
            logger.warning(f"Livekit not compatible with: {type}, defaulting to openai.LLM")
        return openai.LLM(
            model=model,
            **kwargs,
            client=http_client,
        )


async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    return await get_livekit_model(url, type, model, **kwargs)
