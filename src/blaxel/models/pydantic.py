import logging

from anthropic import AsyncAnthropic
from cohere import AsyncClientV2
from mistralai.sdk import Mistral
from pydantic_ai.models import Model
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.cohere import CohereModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.cohere import CohereProvider
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai.providers.openai import OpenAIProvider

from blaxel.common.settings import settings

from ..client import client
from .custom.pydantic.gemini import GoogleGLAProvider

logger = logging.getLogger(__name__)
async def get_pydantic_model(url: str,type: str, model: str, **kwargs) -> Model:
    if type == 'mistral':
        return MistralModel(
            model_name=model,
            provider=MistralProvider(
                mistral_client=Mistral(
                    api_key=settings.auth.token,
                    server_url=url,
                ),
                **kwargs
            ),
        )
    elif type == 'cohere':
        return CohereModel(
            model_name=model,
            provider=CohereProvider(
                cohere_client=AsyncClientV2(
                    api_key=settings.auth.token,
                    base_url=url,
                ),
            ),
        )
    elif type == 'xai':
        return OpenAIModel(
            model_name=model,
            provider=OpenAIProvider(
                base_url=f"{url}/v1",
                api_key=settings.auth.token,
                **kwargs
            ),
        )
    elif type == 'deepseek':
        return OpenAIModel(
            model_name=model,
            provider=OpenAIProvider(
                base_url=f"{url}/v1",
                api_key=settings.auth.token,
                **kwargs
            ),
        )
    elif type == 'cerebras':
        return OpenAIModel(
            model_name=model,
            provider=OpenAIProvider(
                base_url=f"{url}/v1",
                api_key=settings.auth.token,
                **kwargs
            ),
        )
    elif type == 'anthropic':
        return AnthropicModel(
            model_name=model,
            provider=AnthropicProvider(
                anthropic_client=AsyncAnthropic(
                    api_key=settings.auth.token,
                    base_url=url,
                    default_headers=settings.auth.get_headers(),
                ),
                **kwargs
            )
        )
    elif type == 'gemini':
        return GeminiModel(
            model_name=model,
            provider=GoogleGLAProvider(
                api_key=settings.auth.token,
                http_client=client.with_base_url(f"{url}/v1beta/models").get_async_httpx_client()
            )
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by Pydantic, defaulting to OpenAI")
        return OpenAIModel(
            model_name=model,
            provider=OpenAIProvider(
                base_url=f"{url}/v1",
                api_key=settings.auth.token,
                **kwargs
            ),
        )