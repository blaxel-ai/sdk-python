Module blaxel.authentication.clientcredentials
==============================================
This module provides the ClientCredentials class, which handles client credentials-based
authentication for Blaxel. It manages token refreshing and authentication flows using
client credentials and refresh tokens.

Classes
-------

`ClientCredentials(credentials, workspace_name: str, base_url: str)`
:   A provider that authenticates requests using client credentials.
    
    Initializes the ClientCredentials provider with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing access and refresh tokens.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Methods

    `auth_flow(self, request: httpx.Request) ‑> Generator[httpx.Request, httpx.Response, None]`
    :   Processes the authentication flow by ensuring tokens are valid and adding necessary headers.
        
        Parameters:
            request (Request): The HTTP request to authenticate.
        
        Yields:
            Request: The authenticated request.
        
        Raises:
            Exception: If token refresh fails.

    `get_headers(self)`
    :   Retrieves the authentication headers after ensuring tokens are valid.
        
        Returns:
            dict: A dictionary of headers with Bearer token and workspace.
        
        Raises:
            Exception: If token refresh fails.

    `get_token(self) ‑> Exception | None`
    :   Checks if the access token needs to be refreshed and performs the refresh if necessary.
        
        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.

    `need_token(self)`
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