from logging import getLogger

from google.adk.models.lite_llm import LiteLlm, LiteLLMClient

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)


class AuthenticatedLiteLLMClient(LiteLLMClient):
    """Provides acompletion method (for better testability)."""

    async def acompletion(self, model, messages, tools, **kwargs):
        """Asynchronously calls acompletion.

        Args:
          model: The model name.
          messages: The messages to send to the model.
          tools: The tools to use for the model.
          **kwargs: Additional arguments to pass to acompletion.

        Returns:
          The model response as a message.
        """
        kwargs["extra_headers"] = settings.auth.get_headers()
        return await super().acompletion(
            model=model,
            messages=messages,
            tools=tools,
            **kwargs,
        )

    def completion(self, model, messages, tools, stream=False, **kwargs):
        """Synchronously calls completion. This is used for streaming only.

        Args:
          model: The model to use.
          messages: The messages to send.
          tools: The tools to use for the model.
          stream: Whether to stream the response.
          **kwargs: Additional arguments to pass to completion.

        Returns:
          The response from the model.
        """
        kwargs["extra_headers"] = settings.auth.get_headers()
        return super().completion(
            model=model,
            messages=messages,
            tools=tools,
            stream=stream,
            **kwargs,
        )


async def get_google_adk_model(url: str, type: str, model: str, **kwargs):
    print("HEER TWO")
    llm_client = AuthenticatedLiteLLMClient()
    if type == "mistral":
        return LiteLlm(
            model=f"mistral/{model}",
            api_key="replaced",
            api_base=f"{url}/v1",
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "cohere":
        return LiteLlm(
            model=f"cohere/{model}",
            api_base=f"{url}/v2/chat",
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "xai":
        return LiteLlm(
            model=f"xai/{model}",
            api_key="replaced",
            api_base=f"{url}/v1",
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "deepseek":
        return LiteLlm(
            model=f"deepseek/{model}",
            api_key="replaced",
            api_base=f"{url}/v1",
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "anthropic":
        return LiteLlm(
            model=f"anthropic/{model}",
            api_base=url,
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "gemini":
        return LiteLlm(
            model=f"gemini/{model}",
            api_base=f"{url}/v1beta/models/{model}",
            llm_client=llm_client,
            **kwargs,
        )
    elif type == "cerebras":
        return LiteLlm(
            model=f"cerebras/{model}",
            api_key="replaced",
            api_base=f"{url}/v1",
            llm_client=llm_client,
            **kwargs,
        )
    else:
        if type != "openai":
            logger.warning(f"Model {model} is not supported by Google ADK, defaulting to OpenAI")
        return LiteLlm(
            model=f"openai/{model}",
            api_key="replaced",
            api_base=f"{url}/v1",
            llm_client=llm_client,
            **kwargs,
        )


async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    return await get_google_adk_model(url, type, model, **kwargs)
