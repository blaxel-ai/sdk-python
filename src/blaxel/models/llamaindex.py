import os

# Transformers is a dependency of DeepSeek, and it logs a lot of warnings that are not useful
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from logging import getLogger

from google.genai.types import HttpOptions
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.cerebras import Cerebras
from llama_index.llms.deepseek import DeepSeek
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.groq import Groq
from llama_index.llms.mistralai import MistralAI
from llama_index.llms.openai import OpenAI

from ..common.settings import settings
from .custom.llamaindex.cohere import Cohere

logger = getLogger(__name__)

async def get_llamaindex_model(url: str, type: str, model: str, **kwargs):
    if type == 'anthropic':
        return Anthropic(
            model=model,
            api_key=settings.auth.token,
            base_url=url,
            default_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == 'xai':
        return Groq(
            model=model,
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'gemini':
        return GoogleGenAI(
            api_key=settings.auth.token,
            model=model,
            api_base=f"{url}/v1",
            http_options=HttpOptions(
                base_url=url,
                headers=settings.auth.get_headers(),
            ),
            **kwargs
        )
    elif type == 'cohere':
        return Cohere(
            model=model,
            api_key=settings.auth.token,
            api_base=url,
            **kwargs
        )
    elif type == 'deepseek':
        return DeepSeek(
            model=model,
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'mistral':
        return MistralAI(
            model=model,
            api_key=settings.auth.token,
            endpoint=url,
            **kwargs
        )
    elif type == 'cerebras':
        return Cerebras(
            model=model,
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by LlamaIndex, defaulting to OpenAI")

        return OpenAI(
            model=model,
            api_key=settings.auth.token,
            api_base=f"{url}/v1",
            **kwargs
        )