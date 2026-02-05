from logging import getLogger

import httpx
from crewai import LLM  # type: ignore[import-not-found]
from crewai.llms.hooks.base import BaseInterceptor  # type: ignore[import-not-found]

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)


class AuthInterceptor(BaseInterceptor[httpx.Request, httpx.Response]):
    """Interceptor that injects dynamic auth headers into every HTTP request.

    Used for crewai native providers (OpenAI, Anthropic, Gemini, etc.)
    where the LLM.__new__ factory returns a provider-specific instance
    and subclass overrides are not possible.
    """

    def on_outbound(self, message: httpx.Request) -> httpx.Request:
        auth_headers = settings.auth.get_headers()
        # Remove the SDK's default "Authorization: Bearer replaced" header
        # when our auth uses a different header (e.g. X-Blaxel-Authorization with API keys)
        if "Authorization" not in auth_headers:
            message.headers.pop("Authorization", None)
            message.headers.pop("authorization", None)
        for key, value in auth_headers.items():
            message.headers[key] = value
        return message

    def on_inbound(self, message: httpx.Response) -> httpx.Response:
        return message

    async def aon_outbound(self, message: httpx.Request) -> httpx.Request:
        return self.on_outbound(message)

    async def aon_inbound(self, message: httpx.Response) -> httpx.Response:
        return message


# Provider types that crewai routes to native SDK implementations.
# These support the interceptor mechanism for auth.
_NATIVE_PROVIDER_PREFIXES = {"openai", "anthropic", "gemini", "azure", "bedrock"}


def _is_native_route(provider_prefix: str) -> bool:
    """Check if a provider prefix will be routed to a native SDK by crewai."""
    return provider_prefix.lower() in _NATIVE_PROVIDER_PREFIXES


async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()

    # Map blaxel model types to crewai provider prefixes and base URLs
    if type == "mistral":
        provider_prefix = "mistral"
        base_url = f"{url}/v1"
    elif type == "xai":
        provider_prefix = "groq"
        base_url = f"{url}/v1"
    elif type == "deepseek":
        provider_prefix = "openai"
        base_url = f"{url}/v1"
    elif type == "anthropic":
        provider_prefix = "anthropic"
        base_url = url
    elif type == "gemini":
        provider_prefix = "gemini"
        base_url = f"{url}/v1beta/models/{model}"
    elif type == "cerebras":
        provider_prefix = "cerebras"
        base_url = f"{url}/v1"
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by CrewAI, defaulting to OpenAI")
        provider_prefix = "openai"
        base_url = f"{url}/v1"

    model_string = f"{provider_prefix}/{model}"
    auth_headers = settings.auth.get_headers()
    # Only pass api_key when auth uses Authorization header (e.g. OAuth).
    # When auth uses X-Blaxel-Authorization (API keys), omit api_key
    # to prevent "Authorization: Bearer replaced" from being sent.
    llm_api_key = "replaced" if "Authorization" in auth_headers else None

    if _is_native_route(provider_prefix):
        # Native providers: use interceptor for dynamic auth headers
        return LLM(
            model=model_string,
            api_key=llm_api_key,
            base_url=base_url,
            interceptor=AuthInterceptor(),
            **kwargs,
        )
    else:
        # LiteLLM fallback: pass auth headers via extra_headers param
        return LLM(
            model=model_string,
            api_key=llm_api_key,
            base_url=base_url,
            extra_headers=auth_headers,
            **kwargs,
        )
