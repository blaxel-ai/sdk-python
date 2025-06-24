Module blaxel.pydantic.custom.gemini
====================================

Classes
-------

`GoogleGLAProvider(api_key, http_client: httpx.AsyncClient | None = None)`
:   Provider for Google Generative Language AI API.
    
    Create a new Google GLA provider.
    
    Args:
        api_key: The API key to use for authentication, if not provided, the `GEMINI_API_KEY` environment variable
            will be used if available.
        http_client: An existing `httpx.AsyncClient` to use for making HTTP requests.

    ### Ancestors (in MRO)

    * pydantic_ai.providers.Provider
    * abc.ABC
    * typing.Generic

    ### Instance variables

    `base_url: str`
    :   The base URL for the provider API.

    `client: httpx.AsyncClient`
    :   The client for the provider.

    `name`
    :   The provider name.