Module blaxel.authentication
============================

Sub-modules
-----------
* blaxel.authentication.apikey
* blaxel.authentication.authentication
* blaxel.authentication.clientcredentials
* blaxel.authentication.credentials
* blaxel.authentication.device_mode

Functions
---------

`get_authentication_headers(settings: blaxel.common.settings.Settings) ‑> Dict[str, str]`
:   Retrieves authentication headers based on the current context and settings.
    
    Parameters:
        settings (Settings): The settings containing authentication and workspace information.
    
    Returns:
        Dict[str, str]: A dictionary of authentication headers.

`load_credentials(workspace_name: str) ‑> blaxel.authentication.credentials.Credentials`
:   Loads credentials for the specified workspace.
    
    Parameters:
        workspace_name (str): The name of the workspace whose credentials are to be loaded.
    
    Returns:
        Credentials: The credentials associated with the workspace. Returns empty credentials if not found.

`load_credentials_from_settings(settings: blaxel.common.settings.Settings) ‑> blaxel.authentication.credentials.Credentials`
:   Loads credentials from the provided settings.
    
    Parameters:
        settings (Settings): The settings containing authentication information.
    
    Returns:
        Credentials: The loaded credentials from settings.

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

`ApiKeyProvider(credentials, workspace_name: str)`
:   A provider that authenticates requests using an API key.
    
    Initializes the ApiKeyProvider with the given credentials and workspace name.
    
    Parameters:
        credentials: Credentials containing the API key.
        workspace_name (str): The name of the workspace.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Methods

    `auth_flow(self, request: httpx.Request) ‑> Generator[httpx.Request, httpx.Response, None]`
    :   Authenticates the request by adding API key and workspace headers.
        
        Parameters:
            request (Request): The HTTP request to authenticate.
        
        Yields:
            Request: The authenticated request.

    `get_headers(self)`
    :   Retrieves the authentication headers containing the API key and workspace information.
        
        Returns:
            dict: A dictionary of headers with API key and workspace.

`BearerToken(credentials, workspace_name: str, base_url: str)`
:   A provider that authenticates requests using a Bearer token.
    
    Initializes the BearerToken provider with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing the Bearer token and refresh token.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Methods

    `auth_flow(self, request: httpx.Request) ‑> Generator[httpx.Request, httpx.Response, None]`
    :   Processes the authentication flow by ensuring the Bearer token is valid and adding necessary headers.
        
        Parameters:
            request (Request): The HTTP request to authenticate.
        
        Yields:
            Request: The authenticated request.
        
        Raises:
            Exception: If token refresh fails.

    `do_refresh(self) ‑> Exception | None`
    :   Performs the token refresh using the refresh token.
        
        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.

    `get_headers(self) ‑> Dict[str, str]`
    :   Retrieves the authentication headers containing the Bearer token and workspace information.
        
        Returns:
            Dict[str, str]: A dictionary of headers with Bearer token and workspace.
        
        Raises:
            Exception: If token refresh fails.

    `refresh_if_needed(self) ‑> Exception | None`
    :   Checks if the Bearer token needs to be refreshed and performs the refresh if necessary.
        
        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.

`Config(workspaces: List[blaxel.authentication.credentials.WorkspaceConfig] = None, context: blaxel.authentication.credentials.ContextConfig = None)`
:   A dataclass representing the overall configuration, including workspaces and context.
    
    Attributes:
        workspaces (List[WorkspaceConfig]): A list of workspace configurations.
        context (ContextConfig): The current context configuration.

    ### Instance variables

    `context: blaxel.authentication.credentials.ContextConfig`
    :

    `workspaces: List[blaxel.authentication.credentials.WorkspaceConfig]`
    :

    ### Methods

    `to_json(self) ‑> dict`
    :   Converts the Config dataclass to a JSON-compatible dictionary.
        
        Returns:
            dict: The JSON representation of the configuration.

`ContextConfig(workspace: str = '')`
:   A dataclass representing the current context configuration.
    
    Attributes:
        workspace (str): The name of the current workspace.

    ### Instance variables

    `workspace: str`
    :

`Credentials(apiKey: str = '', access_token: str = '', refresh_token: str = '', expires_in: int = 0, device_code: str = '', client_credentials: str = '')`
:   A dataclass representing user credentials for authentication.
    
    Attributes:
        apiKey (str): The API key.
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        expires_in (int): Token expiration time in seconds.
        device_code (str): The device code for device authentication.
        client_credentials (str): The client credentials for authentication.

    ### Instance variables

    `access_token: str`
    :

    `apiKey: str`
    :

    `client_credentials: str`
    :

    `device_code: str`
    :

    `expires_in: int`
    :

    `refresh_token: str`
    :

`DeviceLogin(client_id: str, scope: str)`
:   A dataclass representing a device login request.
    
    Attributes:
        client_id (str): The client ID for the device.
        scope (str): The scope of the authentication.

    ### Instance variables

    `client_id: str`
    :

    `scope: str`
    :

`DeviceLoginFinalizeRequest(grant_type: str, client_id: str, device_code: str)`
:   A dataclass representing a device login finalize request.
    
    Attributes:
        grant_type (str): The type of grant being requested.
        client_id (str): The client ID for finalizing the device login.
        device_code (str): The device code to finalize login.

    ### Instance variables

    `client_id: str`
    :

    `device_code: str`
    :

    `grant_type: str`
    :

`DeviceLoginFinalizeResponse(access_token: str, expires_in: int, refresh_token: str, token_type: str)`
:   DeviceLoginFinalizeResponse(access_token: str, expires_in: int, refresh_token: str, token_type: str)

    ### Instance variables

    `access_token: str`
    :

    `expires_in: int`
    :

    `refresh_token: str`
    :

    `token_type: str`
    :

`DeviceLoginResponse(client_id: str, device_code: str, user_code: str, expires_in: int, interval: int, verification_uri: str, verification_uri_complete: str)`
:   A dataclass representing the response from a device login request.
    
    Attributes:
        client_id (str): The client ID associated with the device login.
        device_code (str): The device code for authentication.
        user_code (str): The user code for completing authentication.
        expires_in (int): Time in seconds until the device code expires.
        interval (int): Polling interval in seconds.
        verification_uri (str): URI for user to verify device login.
        verification_uri_complete (str): Complete URI including the user code for verification.

    ### Instance variables

    `client_id: str`
    :

    `device_code: str`
    :

    `expires_in: int`
    :

    `interval: int`
    :

    `user_code: str`
    :

    `verification_uri: str`
    :

    `verification_uri_complete: str`
    :

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

`WorkspaceConfig(name: str, credentials: blaxel.authentication.credentials.Credentials)`
:   A dataclass representing the configuration for a workspace.
    
    Attributes:
        name (str): The name of the workspace.
        credentials (Credentials): The credentials associated with the workspace.

    ### Instance variables

    `credentials: blaxel.authentication.credentials.Credentials`
    :

    `name: str`
    :