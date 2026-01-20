import os

# Transformers is a dependency of DeepSeek, and it logs a lot of warnings that are not useful
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

from logging import getLogger
from typing import Any, Sequence

from google.genai.types import HttpOptions
from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
)
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.cerebras import Cerebras
from llama_index.llms.deepseek import DeepSeek
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.groq import Groq
from llama_index.llms.mistralai import MistralAI
from llama_index.llms.openai import OpenAI
from llama_index.llms.openai.utils import (
    openai_modelname_to_contextsize as _original_openai_modelname_to_contextsize,
)

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

from .custom.cohere import Cohere

logger = getLogger(__name__)


# Monkey-patch LlamaIndex's model validation to accept any model name
# This is needed for proxy/gateway scenarios where custom model names are used
def _patched_openai_modelname_to_contextsize(modelname: str) -> int:
    """Wrapper that returns a default context size for unknown models."""
    try:
        return _original_openai_modelname_to_contextsize(modelname)
    except ValueError:
        # For unknown models (e.g., from proxies), return a reasonable default
        logger.debug(f"Unknown model '{modelname}', using default context window of 128000")
        return 128000


# Monkey-patch is_chat_model check to recognize unknown models as chat models
from llama_index.llms.openai.utils import is_chat_model as _original_is_chat_model, CHAT_MODELS


def _patched_is_chat_model(model: str) -> bool:
    """Wrapper that defaults to treating unknown models as chat models."""
    result = _original_is_chat_model(model)
    if not result and model not in CHAT_MODELS:
        # Default to chat model for unknown models (modern standard)
        logger.debug(f"Unknown model '{model}', treating as chat model")
        return True
    return result


# Also monkey-patch tiktoken's model lookup for tokenizer validation
import tiktoken
from tiktoken.model import encoding_name_for_model as _original_encoding_name_for_model


def _patched_encoding_name_for_model(model_name: str) -> str:
    """Wrapper that returns a default encoding for unknown models."""
    try:
        return _original_encoding_name_for_model(model_name)
    except KeyError:
        # For unknown models, use the gpt-4o encoding (most modern default)
        logger.debug(f"Unknown model '{model_name}', using default encoding 'o200k_base'")
        return "o200k_base"


# Apply the monkey-patches
import llama_index.llms.openai.utils
import llama_index.llms.openai.base

llama_index.llms.openai.utils.openai_modelname_to_contextsize = _patched_openai_modelname_to_contextsize
llama_index.llms.openai.base.openai_modelname_to_contextsize = _patched_openai_modelname_to_contextsize
llama_index.llms.openai.utils.is_chat_model = _patched_is_chat_model
llama_index.llms.openai.base.is_chat_model = _patched_is_chat_model
tiktoken.model.encoding_name_for_model = _patched_encoding_name_for_model


class TokenRefreshingWrapper:
    """Base wrapper class that refreshes token before each call."""

    def __init__(self, model_config: dict):
        self.model_config = model_config
        self.wrapped_model = self._create_model()

    def _create_model(self):
        """Create the model instance with current token."""
        config = self.model_config
        model_type = config["type"]
        model = config["model"]
        url = config["url"]
        kwargs = config.get("kwargs", {})

        if model_type == "anthropic":
            return Anthropic(
                model=model,
                api_key=settings.auth.token,
                base_url=url,
                default_headers=settings.auth.get_headers(),
                **kwargs,
            )
        elif model_type == "xai":
            return Groq(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "gemini":
            return GoogleGenAI(
                api_key=settings.auth.token,
                model=model,
                api_base=f"{url}/v1",
                http_options=HttpOptions(
                    base_url=url,
                    headers=settings.auth.get_headers(),
                ),
                **kwargs,
            )
        elif model_type == "cohere":
            return Cohere(model=model, api_key=settings.auth.token, api_base=url, **kwargs)
        elif model_type == "deepseek":
            return DeepSeek(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "mistral":
            return MistralAI(model=model, api_key=settings.auth.token, endpoint=url, **kwargs)
        elif model_type == "cerebras":
            return Cerebras(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        else:
            if model_type != "openai":
                logger.warning(
                    f"Model {model} is not supported by LlamaIndex, defaulting to OpenAI"
                )

            # Set default temperature to 1.0 if not specified (some proxies only support default)
            if "temperature" not in kwargs:
                kwargs["temperature"] = 1.0

            return OpenAI(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )

    def _refresh_token(self):
        """Refresh the token and recreate the model if needed."""
        # Only refresh if using ClientCredentials (which has get_token method)
        current_token = settings.auth.token

        if hasattr(settings.auth, "get_token"):
            # This will trigger token refresh if needed
            settings.auth.get_token()

        new_token = settings.auth.token

        # If token changed, recreate the model
        if current_token != new_token:
            self.wrapped_model = self._create_model()

    def __getattr__(self, name):
        """Delegate attribute access to wrapped model."""
        return getattr(self.wrapped_model, name)


class TokenRefreshingLLM(TokenRefreshingWrapper):
    """Wrapper for LlamaIndex LLMs that refreshes token before each call."""

    async def achat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        """Async chat with token refresh."""
        self._refresh_token()
        return await self.wrapped_model.achat(messages, **kwargs)

    def chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        """Sync chat with token refresh."""
        self._refresh_token()
        return self.wrapped_model.chat(messages, **kwargs)

    async def astream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        """Async stream chat with token refresh."""
        self._refresh_token()
        async for chunk in self.wrapped_model.astream_chat(messages, **kwargs):
            yield chunk

    def stream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseGen:
        """Sync stream chat with token refresh."""
        self._refresh_token()
        for chunk in self.wrapped_model.stream_chat(messages, **kwargs):
            yield chunk

    async def acomplete(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> CompletionResponse:
        """Async complete with token refresh."""
        self._refresh_token()
        return await self.wrapped_model.acomplete(prompt, **kwargs)

    def complete(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> CompletionResponse:
        """Sync complete with token refresh."""
        self._refresh_token()
        return self.wrapped_model.complete(prompt, **kwargs)

    async def astream_complete(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> CompletionResponseAsyncGen:
        """Async stream complete with token refresh."""
        self._refresh_token()
        async for chunk in self.wrapped_model.astream_complete(prompt, **kwargs):
            yield chunk

    def stream_complete(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> CompletionResponseGen:
        """Sync stream complete with token refresh."""
        self._refresh_token()
        for chunk in self.wrapped_model.stream_complete(prompt, **kwargs):
            yield chunk


async def bl_model(name, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()

    # Store model configuration for recreation
    model_config = {"type": type, "model": model, "url": url, "kwargs": kwargs}

    # Create and return the wrapper
    return TokenRefreshingLLM(model_config)
