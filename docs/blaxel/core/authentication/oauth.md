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
:   OauthTokenData(body: dict[str, typing.Optional[str]] = <factory>, headers: dict[str, str] = <factory>, authenticated: Optional[bool] = False)

    ### Instance variables

    `authenticated: bool | None`
    :

    `body: dict[str, str | None]`
    :

    `headers: dict[str, str]`
    :

`OauthTokenError(error: str)`
:   OauthTokenError(error: str)

    ### Instance variables

    `error: str`
    :

`OauthTokenResponse(access_token: str, refresh_token: str, expires_in: int, token_type: str)`
:   OauthTokenResponse(access_token: str, refresh_token: str, expires_in: int, token_type: str)

    ### Instance variables

    `access_token: str`
    :

    `expires_in: int`
    :

    `refresh_token: str`
    :

    `token_type: str`
    :