Module blaxel.core.authentication
=================================

Sub-modules
-----------
* blaxel.core.authentication.apikey
* blaxel.core.authentication.clientcredentials
* blaxel.core.authentication.devicemode
* blaxel.core.authentication.oauth
* blaxel.core.authentication.types

Classes
-------

`BlaxelAuth(credentials: blaxel.core.authentication.types.CredentialsType, workspace_name: str, base_url: str)`
:   Base class for all authentication schemes.
    
    To implement a custom authentication scheme, subclass `Auth` and override
    the `.auth_flow()` method.
    
    If the authentication scheme does I/O such as disk access or network calls, or uses
    synchronization primitives such as locks, you should override `.sync_auth_flow()`
    and/or `.async_auth_flow()` instead of `.auth_flow()` to provide specialized
    implementations that will be used by `Client` and `AsyncClient` respectively.
    
    Initializes the BlaxelAuth with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing the Bearer token and refresh token.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Descendants

    * blaxel.core.authentication.apikey.ApiKey
    * blaxel.core.authentication.clientcredentials.ClientCredentials
    * blaxel.core.authentication.devicemode.DeviceMode

    ### Instance variables

    `token`
    :

    ### Methods

    `get_headers(self) ‑> Dict[str, str]`
    :

`CredentialsType(**data: Any)`
:   Represents authentication credentials for the API
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `access_token: str | None`
    :

    `api_key: str | None`
    :

    `client_credentials: str | None`
    :

    `device_code: str | None`
    :

    `expires_in: int | None`
    :

    `model_config`
    :

    `refresh_token: str | None`
    :

    `workspace: str | None`
    :