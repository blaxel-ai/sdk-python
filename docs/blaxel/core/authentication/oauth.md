Module blaxel.core.authentication.oauth
=======================================

Functions
---------

`oauth_token(options: blaxel.core.authentication.oauth.OauthTokenData, client: blaxel.core.client.client.Client | None = None, throw_on_error: bool = False) ‑> blaxel.core.authentication.oauth.OauthTokenResponse | blaxel.core.authentication.oauth.OauthTokenError`
:   Get a new OAuth token.
    
    Args:
        options: The OAuth token request options
        client: Optional client instance to use for the request
        throw_on_error: Whether to throw an exception on error
    
    Returns:
        The OAuth token response or error

Classes
-------

`OauthTokenData(body: dict[str, str | None] = <factory>, headers: dict[str, str] = <factory>, authenticated: bool | None = False)`
:   OauthTokenData(body: dict[str, typing.Optional[str]] = <factory>, headers: dict[str, str] = <factory>, authenticated: bool | None = False)

    ### Instance variables

    `authenticated: bool | None`
    :   The type of the None singleton.

    `body: dict[str, str | None]`
    :   The type of the None singleton.

    `headers: dict[str, str]`
    :   The type of the None singleton.

`OauthTokenError(error: str)`
:   OauthTokenError(error: str)

    ### Instance variables

    `error: str`
    :   The type of the None singleton.

`OauthTokenResponse(access_token: str, refresh_token: str, expires_in: int, token_type: str)`
:   OauthTokenResponse(access_token: str, refresh_token: str, expires_in: int, token_type: str)

    ### Instance variables

    `access_token: str`
    :   The type of the None singleton.

    `expires_in: int`
    :   The type of the None singleton.

    `refresh_token: str`
    :   The type of the None singleton.

    `token_type: str`
    :   The type of the None singleton.