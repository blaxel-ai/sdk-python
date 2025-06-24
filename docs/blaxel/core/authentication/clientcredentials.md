Module blaxel.core.authentication.clientcredentials
===================================================
This module provides the ClientCredentials class, which handles client credentials-based
authentication for Blaxel. It manages token refreshing and authentication flows using
client credentials and refresh tokens.

Classes
-------

`ClientCredentials(credentials: blaxel.core.authentication.types.CredentialsType, workspace_name: str, base_url: str)`
:   ClientCredentials auth that authenticates requests using client credentials.
    
    Initializes the BlaxelAuth with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing the Bearer token and refresh token.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * blaxel.core.authentication.types.BlaxelAuth
    * httpx.Auth

    ### Class variables

    `expires_at: datetime.datetime | None`
    :

    ### Instance variables

    `token`
    :

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
        Uses recursive retry logic for up to 3 attempts.
        
        Returns:
            Optional[Exception]: An exception if refreshing fails after all retries, otherwise None.

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