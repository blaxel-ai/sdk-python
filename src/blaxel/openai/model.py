import httpx
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings


class DynamicHeadersHTTPClient(httpx.AsyncClient):
    """Custom HTTP client that dynamically updates headers on each request."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send(self, request, *args, **kwargs):
        # Update headers with the latest auth headers before each request
        auth_headers = settings.auth.get_headers()
        for key, value in auth_headers.items():
            request.headers[key] = value
        return await super().send(request, *args, **kwargs)


async def bl_model(name, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    if type != "openai":
        raise ValueError(f"Invalid model type: {type}")

    # Create custom HTTP client with dynamic headers
    http_client = DynamicHeadersHTTPClient(
        base_url=f"{url}/v1",
    )

    external_client = AsyncOpenAI(
        base_url=f"{url}/v1",
        api_key="replaced",
        http_client=http_client,
    )

    return OpenAIChatCompletionsModel(model=model, openai_client=external_client, **kwargs)
