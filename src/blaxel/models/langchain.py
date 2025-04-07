from logging import getLogger

from langchain_anthropic import ChatAnthropic
from langchain_cerebras import ChatCerebras
from langchain_cohere import ChatCohere
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_xai import ChatXAI

from ..common.settings import settings
from .custom.langchain.gemini import ChatGoogleGenerativeAI

logger = getLogger(__name__)

async def get_langchain_model(url: str,type: str, model: str, **kwargs):
    if type == 'mistral':
        return ChatOpenAI(
            api_key=settings.auth.token,
            model=model,
            base_url=f"{url}/v1",
            **kwargs
        )
    elif type == 'cohere':
        return ChatCohere(
            cohere_api_key=settings.auth.token,
            model=model,
            base_url=url,
            **kwargs
        )
    elif type == 'xai':
        return ChatXAI(
            model=model,
            api_key=settings.auth.token,
            xai_api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'deepseek':
        return ChatDeepSeek(
            api_key=settings.auth.token,
            model=model,
            api_base=f"{url}/v1",
            **kwargs
        )
    elif type == 'anthropic':
        return ChatAnthropic(
            api_key=settings.auth.token,
            anthropic_api_url=url,
            model=model,
            default_headers=settings.auth.get_headers(),
            **kwargs
        )
    elif type == 'gemini':
        return ChatGoogleGenerativeAI(
            model=model,
            client_options={"api_endpoint": url},
            additional_headers=settings.auth.get_headers(),
            transport="rest",
            **kwargs
        )
    elif type == "cerebras":
        return ChatCerebras(
            api_key=settings.auth.token,
            model=model,
            base_url=f"{url}/v1",
            **kwargs
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by Langchain, defaulting to OpenAI")
        return ChatOpenAI(
            api_key=settings.auth.token,
            model=model,
            base_url=f"{url}/v1",
            **kwargs
        )
