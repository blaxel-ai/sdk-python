from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator, List

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

if TYPE_CHECKING:
    from langchain_core.callbacks import Callbacks  # type: ignore[import-not-found]
    from langchain_core.language_models import (  # type: ignore[import-not-found]
        LanguageModelInput,
    )
    from langchain_core.messages import BaseMessage  # type: ignore[import-not-found]
    from langchain_core.outputs import LLMResult  # type: ignore[import-not-found]
    from langchain_core.runnables import (  # type: ignore[import-not-found]
        RunnableConfig,
    )

logger = getLogger(__name__)


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

        if model_type == "mistral":
            from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]

            return ChatOpenAI(
                api_key=settings.auth.token,
                model=model,
                base_url=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "cohere":
            from langchain_cohere import ChatCohere  # type: ignore[import-not-found]

            return ChatCohere(
                cohere_api_key=settings.auth.token,
                model=model,
                base_url=url,
                **kwargs,
            )
        elif model_type == "xai":
            from langchain_xai import ChatXAI  # type: ignore[import-not-found]

            return ChatXAI(
                model=model,
                api_key=settings.auth.token,
                xai_api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "deepseek":
            from langchain_deepseek import (  # type: ignore[import-not-found]
                ChatDeepSeek,
            )

            return ChatDeepSeek(
                api_key=settings.auth.token,
                model=model,
                api_base=f"{url}/v1",
                **kwargs,
            )
        elif model_type == "anthropic":
            from langchain_anthropic import (  # type: ignore[import-not-found]
                ChatAnthropic,
            )

            return ChatAnthropic(
                api_key=settings.auth.token,
                anthropic_api_url=url,
                model=model,
                default_headers=settings.auth.get_headers(),
                **kwargs,
            )
        elif model_type == "gemini":
            from .custom.gemini import (
                ChatGoogleGenerativeAI,  # type: ignore[import-not-found]
            )

            return ChatGoogleGenerativeAI(
                model=model,
                client_options={"api_endpoint": url},
                additional_headers=settings.auth.get_headers(),
                transport="rest",
                **kwargs,
            )
        elif model_type == "cerebras":
            from langchain_cerebras import (  # type: ignore[import-not-found]
                ChatCerebras,
            )

            return ChatCerebras(
                api_key=settings.auth.token,
                model=model,
                base_url=f"{url}/v1",
                **kwargs,
            )
        else:
            from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]

            if model_type != "openai":
                logger.warning(f"Model {model} is not supported by Langchain, defaulting to OpenAI")
            return ChatOpenAI(
                api_key=settings.auth.token,
                model=model,
                base_url=f"{url}/v1",
                **kwargs,
            )

    def _refresh_token(self):
        """Refresh the token and recreate the model if needed."""
        # Only refresh if using ClientCredentials (which has get_token method)
        current_token = settings.auth.token

        new_token = settings.auth.token

        # If token changed, recreate the model
        if current_token != new_token:
            self.wrapped_model = self._create_model()

    def __getattr__(self, name):
        """Delegate attribute access to wrapped model."""
        return getattr(self.wrapped_model, name)


class TokenRefreshingChatModel(TokenRefreshingWrapper):
    """Wrapper for chat models that refreshes token before each call."""

    async def ainvoke(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        *,
        stop: List[str] | None = None,
        **kwargs: Any,
    ) -> BaseMessage:
        """Async invoke with token refresh."""
        self._refresh_token()
        return await self.wrapped_model.ainvoke(input, config, stop=stop, **kwargs)

    def invoke(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        *,
        stop: List[str] | None = None,
        **kwargs: Any,
    ) -> BaseMessage:
        """Sync invoke with token refresh."""
        self._refresh_token()
        return self.wrapped_model.invoke(input, config, stop=stop, **kwargs)

    async def astream(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        *,
        stop: List[str] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[BaseMessage]:
        """Async stream with token refresh."""
        self._refresh_token()
        async for chunk in self.wrapped_model.astream(input, config, stop=stop, **kwargs):
            yield chunk

    def stream(
        self,
        input: LanguageModelInput,
        config: RunnableConfig | None = None,
        *,
        stop: List[str] | None = None,
        **kwargs: Any,
    ) -> Iterator[BaseMessage]:
        """Sync stream with token refresh."""
        self._refresh_token()
        for chunk in self.wrapped_model.stream(input, config, stop=stop, **kwargs):
            yield chunk

    async def agenerate(
        self,
        messages: List[List[BaseMessage]],
        stop: List[str] | None = None,
        callbacks: Callbacks = None,
        *,
        tags: List[str] | None = None,
        metadata: dict[str, Any] | None = None,
        run_name: str | None = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Async generate with token refresh."""
        self._refresh_token()
        return await self.wrapped_model.agenerate(
            messages,
            stop=stop,
            callbacks=callbacks,
            tags=tags,
            metadata=metadata,
            run_name=run_name,
            **kwargs,
        )

    def generate(
        self,
        messages: List[List[BaseMessage]],
        stop: List[str] | None = None,
        callbacks: Callbacks = None,
        *,
        tags: List[str] | None = None,
        metadata: dict[str, Any] | None = None,
        run_name: str | None = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Sync generate with token refresh."""
        self._refresh_token()
        return self.wrapped_model.generate(
            messages,
            stop=stop,
            callbacks=callbacks,
            tags=tags,
            metadata=metadata,
            run_name=run_name,
            **kwargs,
        )

    async def astream_events(self, *args, **kwargs):
        """Async stream events with token refresh."""
        self._refresh_token()
        async for event in self.wrapped_model.astream_events(*args, **kwargs):
            yield event

    def batch(self, *args, **kwargs):
        """Batch with token refresh."""
        self._refresh_token()
        return self.wrapped_model.batch(*args, **kwargs)

    async def abatch(self, *args, **kwargs):
        """Async batch with token refresh."""
        self._refresh_token()
        return await self.wrapped_model.abatch(*args, **kwargs)


async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()

    # Store model configuration for recreation
    model_config = {"type": type, "model": model, "url": url, "kwargs": kwargs}

    # Create and return the wrapper
    return TokenRefreshingChatModel(model_config)