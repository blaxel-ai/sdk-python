
import httpx
from httpx import AsyncClient
from pydantic_ai.providers import Provider


class GoogleGLAProvider(Provider[AsyncClient]):
    """Provider for Google Generative Language AI API."""

    @property
    def name(self):
        return 'google-gla'

    @property
    def base_url(self) -> str:
        return 'https://generativelanguage.googleapis.com/v1beta/models/'

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    def __init__(self, api_key, http_client: httpx.AsyncClient | None = None) -> None:
        """Create a new Google GLA provider.

        Args:
            api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
                will be used if available.
            http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.
        """
        self._client = http_client
        # https://cloud.google.com/docs/authentication/api-keys-use#using-with-rest
        self._client.headers['X-Goog-Api-Key'] = api_key
