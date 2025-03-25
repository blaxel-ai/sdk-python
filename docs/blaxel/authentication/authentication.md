Module blaxel.authentication.authentication
===========================================
This module provides classes and functions for handling various authentication methods,
including public access, API key authentication, client credentials, and bearer tokens.
It also includes utilities for creating authenticated clients and managing authentication headers.

Functions
---------

`get_authentication_headers(settings: blaxel.common.settings.Settings) ‑> Dict[str, str]`
:   Retrieves authentication headers based on the current context and settings.
    
    Parameters:
        settings (Settings): The settings containing authentication and workspace information.
    
    Returns:
        Dict[str, str]: A dictionary of authentication headers.

`new_client()`
:   Creates a new authenticated client based on the current context and settings.
    
    Returns:
        AuthenticatedClient: An instance of AuthenticatedClient configured with the current context or settings.

`new_client_from_settings(settings: blaxel.common.settings.Settings)`
:   Creates a new authenticated client using the provided settings.
    
    Parameters:
        settings (Settings): The settings containing authentication and workspace information.
    
    Returns:
        AuthenticatedClient: An instance of AuthenticatedClient configured with the provided settings.

`new_client_with_credentials(config: blaxel.authentication.authentication.RunClientWithCredentials)`
:   Creates a new authenticated client using the provided client configuration.
    
    Parameters:
        config (RunClientWithCredentials): The client configuration containing credentials and workspace information.
    
    Returns:
        AuthenticatedClient: An instance of AuthenticatedClient configured with the provided credentials.

Classes
-------

`PublicProvider()`
:   A provider that allows public access without any authentication.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Methods

    `auth_flow(self, request: httpx.Request) ‑> Generator[httpx.Request, httpx.Response, None]`
    :   Processes the authentication flow for public access by yielding the request as-is.
        
        Parameters:
            request (Request): The HTTP request to process.
        
        Yields:
            Request: The unmodified request.

`RunClientWithCredentials(credentials: blaxel.authentication.credentials.Credentials, workspace: str, api_url: str = '', run_url: str = '')`
:   A dataclass that holds credentials and workspace information for initializing an authenticated client.
    
    Attributes:
        credentials (Credentials): The credentials used for authentication.
        workspace (str): The name of the workspace.
        api_url (str): The base API URL.
        run_url (str): The run-specific URL.

    ### Instance variables

    `api_url: str`
    :

    `credentials: blaxel.authentication.credentials.Credentials`
    :

    `run_url: str`
    :

    `workspace: str`
    :