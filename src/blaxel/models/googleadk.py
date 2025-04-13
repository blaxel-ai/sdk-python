from logging import getLogger

from google.adk.models.lite_llm import LiteLlm

from ..common.settings import settings

logger = getLogger(__name__)

async def get_google_adk_model(url: str, type: str, model: str, **kwargs):
    if type == 'mistral':
        return LiteLlm(
            model=f"mistral/{model}",
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'cohere':
        return LiteLlm(
            model=f"cohere/{model}",
            api_base=f"{url}/v2/chat",
            extra_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == 'xai':
        return LiteLlm(
            model=f"xai/{model}",
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'deepseek':
        return LiteLlm(
            model=f"deepseek/{model}",
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'anthropic':
        return LiteLlm(
            model=f"anthropic/{model}",
            api_base=url,
            extra_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == 'gemini':
        return LiteLlm(
            model=f"gemini/{model}",
            api_base=f"{url}/v1beta/models/{model}",
            extra_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == "cerebras":
        return LiteLlm(
            model=f"cerebras/{model}",
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by Google ADK, defaulting to OpenAI")
        return LiteLlm(
            model=f"openai/{model}",
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )