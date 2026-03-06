from __future__ import annotations

import os
from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Union

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

# Transformers is a dependency of DeepSeek, and it logs a lot of warnings that are not useful
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

if TYPE_CHECKING:
    from llama_index.core.base.llms.types import (  # type: ignore[import-not-found]
        ChatMessage,
        ChatResponse,
        ChatResponseAsyncGen,
        ChatResponseGen,
        CompletionResponse,
        CompletionResponseAsyncGen,
        CompletionResponseGen,
    )
    from llama_index.core.llms.llm import (  # type: ignore[import-not-found]
        ToolSelection,
    )
    from llama_index.core.tools.types import BaseTool  # type: ignore[import-not-found]

# Runtime imports needed for class inheritance and construction
from llama_index.core.base.llms.types import (  # type: ignore[import-not-found]
    LLMMetadata,
)
from llama_index.core.llms.function_calling import (  # type: ignore[import-not-found]
    FunctionCallingLLM,
)
from pydantic import PrivateAttr  # type: ignore[import-not-found]

logger = getLogger(__name__)

DEFAULT_CONTEXT_WINDOW = 128000
DEFAULT_NUM_OUTPUT = 4096


class TokenRefreshingLLM(FunctionCallingLLM):
    """Wrapper for LlamaIndex LLMs that refreshes token before each call.

    Inherits from FunctionCallingLLM to maintain type compatibility with
    LlamaIndex's agents and components that validate isinstance(model, LLM).
    """

    _model_config_data: dict = PrivateAttr(default_factory=dict)
    _wrapped: Any = PrivateAttr(default=None)

    def __init__(self, model_config: dict):
        super().__init__()
        self._model_config_data = model_config
        self._wrapped = self._create_model()

    @classmethod
    def class_name(cls) -> str:
        return "TokenRefreshingLLM"

    @property
    def wrapped_model(self) -> Any:
        """Access the underlying wrapped LLM model."""
        return self._wrapped

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata, with fallback for unknown model names."""
        try:
            return self._wrapped.metadata
        except (ValueError, KeyError) as e:
            logger.warning(f"Could not get metadata from wrapped model: {e}. Using defaults.")
            return LLMMetadata(
                context_window=DEFAULT_CONTEXT_WINDOW,
                num_output=DEFAULT_NUM_OUTPUT,
                is_chat_model=True,
                model_name=self._model_config_data.get("model", "unknown"),
            )

    def _create_model(self):
        """Create the model instance with current token."""
        config = self._model_config_data
        model_type = config["type"]
        model = config["model"]
        url = config["url"]
        kwargs = config.get("kwargs", {})

        if model_type == "anthropic":
            from llama_index.llms.anthropic import (  # type: ignore[import-not-found]
                Anthropic,
            )

            return Anthropic(
                model=model,
                api_key=settings.auth.token,
                base_url=url,
                default_headers=settings.auth.get_headers(),
                **kwargs,
            )
        elif model_type == "xai":
            from llama_index.llms.groq import Groq  # type: ignore[import-not-found]

            return Groq(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "gemini":
            from google.genai.types import HttpOptions
            from llama_index.llms.google_genai import (  # type: ignore[import-not-found]
                GoogleGenAI,
            )

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
            from .custom.cohere import Cohere  # type: ignore[import-not-found]

            return Cohere(model=model, api_key=settings.auth.token, api_base=url, **kwargs)
        elif model_type == "deepseek":
            from llama_index.llms.deepseek import (  # type: ignore[import-not-found]
                DeepSeek,
            )

            return DeepSeek(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "mistral":
            from llama_index.llms.mistralai import (  # type: ignore[import-not-found]
                MistralAI,
            )

            return MistralAI(model=model, api_key=settings.auth.token, endpoint=url, **kwargs)
        elif model_type == "cerebras":
            from llama_index.llms.cerebras import (  # type: ignore[import-not-found]
                Cerebras,
            )

            return Cerebras(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )
        else:
            from llama_index.llms.openai import OpenAI  # type: ignore[import-not-found]

            if model_type != "openai":
                logger.warning(
                    f"Model {model} is not supported by LlamaIndex, defaulting to OpenAI"
                )

            return OpenAI(
                model=model,
                api_key=settings.auth.token,
                api_base=f"{url}/v1",
                **kwargs,
            )

    def _refresh_token(self):
        """Refresh the token and recreate the model if needed."""
        current_token = settings.auth.token

        new_token = settings.auth.token

        if current_token != new_token:
            self._wrapped = self._create_model()

    # --- Core LLM methods with token refresh ---

    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        self._refresh_token()
        return self._wrapped.chat(messages, **kwargs)

    async def achat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        self._refresh_token()
        return await self._wrapped.achat(messages, **kwargs)

    def complete(self, prompt: str, formatted: bool = False, **kwargs: Any) -> CompletionResponse:
        self._refresh_token()
        return self._wrapped.complete(prompt, formatted=formatted, **kwargs)

    async def acomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        self._refresh_token()
        return await self._wrapped.acomplete(prompt, formatted=formatted, **kwargs)

    def stream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseGen:
        self._refresh_token()
        return self._wrapped.stream_chat(messages, **kwargs)

    async def astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        self._refresh_token()
        result = self._wrapped.astream_chat(messages, **kwargs)
        # Handle both coroutine and async generator patterns
        if hasattr(result, "__aiter__"):
            return result
        return await result

    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        self._refresh_token()
        return self._wrapped.stream_complete(prompt, formatted=formatted, **kwargs)

    async def astream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        self._refresh_token()
        result = self._wrapped.astream_complete(prompt, formatted=formatted, **kwargs)
        # Handle both coroutine and async generator patterns
        if hasattr(result, "__aiter__"):
            return result
        return await result

    # --- FunctionCallingLLM methods (delegate to wrapped model) ---

    def _prepare_chat_with_tools(
        self,
        tools: Sequence[BaseTool],
        user_msg: Union[str, ChatMessage, None] = None,
        chat_history: List[ChatMessage] | None = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        tool_required: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if hasattr(self._wrapped, "_prepare_chat_with_tools"):
            return self._wrapped._prepare_chat_with_tools(
                tools,
                user_msg=user_msg,
                chat_history=chat_history,
                verbose=verbose,
                allow_parallel_tool_calls=allow_parallel_tool_calls,
                tool_required=tool_required,
                **kwargs,
            )
        raise NotImplementedError(
            f"The wrapped model ({type(self._wrapped).__name__}) does not support function calling"
        )

    def get_tool_calls_from_response(
        self,
        response: ChatResponse,
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
        if hasattr(self._wrapped, "get_tool_calls_from_response"):
            return self._wrapped.get_tool_calls_from_response(
                response,
                error_on_no_tool_call=error_on_no_tool_call,
                **kwargs,
            )
        raise NotImplementedError(
            f"The wrapped model ({type(self._wrapped).__name__}) does not support function calling"
        )


async def bl_model(name, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()

    # Store model configuration for recreation
    model_config = {"type": type, "model": model, "url": url, "kwargs": kwargs}

    # Create and return the wrapper
    return TokenRefreshingLLM(model_config)
