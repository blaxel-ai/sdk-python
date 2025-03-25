Module blaxel.authentication.apikey
===================================
This module provides the ApiKeyProvider class, which handles API key-based authentication for Blaxel.

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