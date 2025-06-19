Module blaxel.core.authentication.apikey
========================================
This module provides the ApiKey class, which handles API key-based authentication for Blaxel.

Classes
-------

`ApiKey(credentials: blaxel.core.authentication.types.CredentialsType, workspace_name: str, base_url: str)`
:   ApiKey auth that authenticates requests using an API key.
    
    Initializes the BlaxelAuth with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing the Bearer token and refresh token.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * blaxel.core.authentication.types.BlaxelAuth
    * httpx.Auth

    ### Instance variables

    `token`
    :

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