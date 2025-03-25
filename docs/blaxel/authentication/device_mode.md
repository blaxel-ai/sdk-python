Module blaxel.authentication.device_mode
========================================
This module provides classes for handling device-based authentication,
including device login processes and bearer token management. It facilitates token refreshing
and authentication flows using device codes and bearer tokens.

Classes
-------

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