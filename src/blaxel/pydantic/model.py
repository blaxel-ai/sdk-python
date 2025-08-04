import logging
from typing import Any, Optional

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

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings
from blaxel.core.client import client

from .custom.gemini import GoogleGLAProvider

logger = logging.getLogger(__name__)


class TokenRefreshingModel(Model):
    """Model wrapper that transparently refreshes tokens before each API call."""

    def __init__(self, model_config: dict):
        self.model_config = model_config
        self._cached_model = None
        self._cached_token = None

    def _create_model(self) -> Model:
        """Create the model instance with current token."""
        config = self.model_config
        type = config["type"]
        model = config["model"]
        url = config["url"]
        kwargs = config.get("kwargs", {})

        if type == "mistral":
            return MistralModel(
                model_name=model,
                provider=MistralProvider(
                    mistral_client=Mistral(
                        api_key=settings.auth.token,
                        server_url=url,
                    ),
                    **kwargs,
                ),
            )
        elif type == "cohere":
            return CohereModel(
                model_name=model,
                provider=CohereProvider(
                    cohere_client=AsyncClientV2(
                        api_key=settings.auth.token,
                        base_url=url,
                    ),
                ),
            )
        elif type == "xai":
            return OpenAIModel(
                model_name=model,
                provider=OpenAIProvider(
                    base_url=f"{url}/v1", api_key=settings.auth.token, **kwargs
                ),
            )
        elif type == "deepseek":
            return OpenAIModel(
                model_name=model,
                provider=OpenAIProvider(
                    base_url=f"{url}/v1", api_key=settings.auth.token, **kwargs
                ),
            )
        elif type == "cerebras":
            return OpenAIModel(
                model_name=model,
                provider=OpenAIProvider(
                    base_url=f"{url}/v1", api_key=settings.auth.token, **kwargs
                ),
            )
        elif type == "anthropic":
            return AnthropicModel(
                model_name=model,
                provider=AnthropicProvider(
                    anthropic_client=AsyncAnthropic(
                        api_key=settings.auth.token,
                        base_url=url,
                        default_headers=settings.auth.get_headers(),
                    ),
                    **kwargs,
                ),
            )
        elif type == "gemini":
            return GeminiModel(
                model_name=model,
                provider=GoogleGLAProvider(
                    api_key=settings.auth.token,
                    http_client=client.with_base_url(
                        f"{url}/v1beta/models"
                    ).get_async_httpx_client(),
                ),
            )
        else:
            if type != "openai":
                logger.warning(f"Model {model} is not supported by Pydantic, defaulting to OpenAI")
            return OpenAIModel(
                model_name=model,
                provider=OpenAIProvider(
                    base_url=f"{url}/v1", api_key=settings.auth.token, **kwargs
                ),
            )

    def _get_fresh_model(self) -> Model:
        """Get or create a model with fresh token if needed."""
        # Only refresh if using ClientCredentials (which has get_token method)
        if hasattr(settings.auth, "get_token"):
            # This will trigger token refresh if needed
            logger.debug(f"Calling get_token for {self.model_config['type']} model")
            settings.auth.get_token()

        new_token = settings.auth.token

        # If token changed or no cached model, create new one
        if self._cached_token != new_token or self._cached_model is None:
            self._cached_model = self._create_model()
            self._cached_token = new_token

        return self._cached_model

    @property
    def model_name(self) -> str:
        """Return the model name."""
        model = self._get_fresh_model()
        return model.model_name

    @property
    def system(self) -> Optional[Any]:
        """Return the system property from the wrapped model."""
        model = self._get_fresh_model()
        return model.system if hasattr(model, "system") else None

    async def request(self, *args, **kwargs):
        """Make a request to the model with token refresh."""
        model = self._get_fresh_model()
        # Pass all arguments through to the wrapped model
        return await model.request(*args, **kwargs)

    def __getattr__(self, name):
        """Delegate any other attributes to the wrapped model."""
        # Get fresh model in case token changed
        model = self._get_fresh_model()
        return getattr(model, name)


async def bl_model(name: str, **kwargs) -> Model:
    """Create a Pydantic AI model with automatic token refresh support."""
    url, type, model = await bl_model_core(name).get_parameters()

    # Store model configuration for recreation
    model_config = {"type": type, "model": model, "url": url, "kwargs": kwargs}

    # Create and return the wrapper
    return TokenRefreshingModel(model_config)
