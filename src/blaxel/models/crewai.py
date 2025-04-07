from logging import getLogger

from crewai import LLM

from ..common.settings import settings

logger = getLogger(__name__)

async def get_crewai_model(url: str, type: str, model: str, **kwargs):
    if type == 'mistral':
        return LLM(
            model=f"mistral/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
    elif type == 'xai':
        return LLM(
            model=f"groq/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
    elif type == 'deepseek':
        return LLM(
            model=f"openai/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
    elif type == 'anthropic':
        return LLM(
            model=f"anthropic/{model}",
            api_key=settings.auth.token,
            base_url=url,
            extra_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == 'gemini':
        return LLM(
            model=f"gemini/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1beta/models/{model}",
            **kwargs
        )
    elif type == 'cerebras':
        return LLM(
            model=f"cerebras/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by CrewAI, defaulting to OpenAI")
        return LLM(
            model=f"openai/{model}",
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
