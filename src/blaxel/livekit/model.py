from logging import getLogger

import httpx
from livekit.plugins import openai
from openai import AsyncOpenAI

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)


class DynamicHeadersHTTPClient(httpx.AsyncClient):
    """Custom HTTP client that dynamically updates headers on each request."""

    def __init__(self, base_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    async def send(self, request, *args, **kwargs):
        # Update headers with the latest auth headers before each request
        auth_headers = settings.auth.get_headers()
        for key, value in auth_headers.items():
            request.headers[key] = value
        print(request.__dict__)
        return await super().send(request, *args, **kwargs)


async def get_livekit_model(url: str, type: str, model: str, **kwargs):
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
