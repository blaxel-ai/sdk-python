from logging import getLogger

from crewai import LLM

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)


class AuthenticatedLLM(LLM):
    def call(self, *args, **kwargs):
        self.additional_params["extra_headers"] = settings.auth.get_headers()
        return super().call(*args, **kwargs)


async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    if type == "mistral":
        return AuthenticatedLLM(
            model=f"mistral/{model}", api_key="replaced", base_url=f"{url}/v1", **kwargs
        )
    elif type == "xai":
        return AuthenticatedLLM(
            model=f"groq/{model}", api_key="replaced", base_url=f"{url}/v1", **kwargs
        )
    elif type == "deepseek":
        return AuthenticatedLLM(
            model=f"openai/{model}", api_key="replaced", base_url=f"{url}/v1", **kwargs
        )
    elif type == "anthropic":
        return AuthenticatedLLM(
            model=f"anthropic/{model}",
            api_key="replaced",
            base_url=url,
            **kwargs,
        )
    elif type == "gemini":
        return AuthenticatedLLM(
            model=f"gemini/{model}",
            api_key="replaced",
            base_url=f"{url}/v1beta/models/{model}",
            **kwargs,
        )
    elif type == "cerebras":
        return AuthenticatedLLM(
            model=f"cerebras/{model}", api_key="replaced", base_url=f"{url}/v1", **kwargs
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by CrewAI, defaulting to OpenAI")
        return AuthenticatedLLM(
            model=f"openai/{model}", api_key="replaced", base_url=f"{url}/v1", **kwargs
        )
