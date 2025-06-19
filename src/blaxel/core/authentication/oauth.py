from dataclasses import dataclass, field
from typing import Optional, Union

from ..client import Client
from ..client import client as default_client


@dataclass
class OauthTokenData:
    body: dict[str, Union[str, Optional[str]]] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    authenticated: Optional[bool] = False

@dataclass
class OauthTokenResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

@dataclass
class OauthTokenError:
    error: str

async def oauth_token(
    options: OauthTokenData,
    client: Optional[Client] = None,
    throw_on_error: bool = False
) -> Union[OauthTokenResponse, OauthTokenError]:
    """
    Get a new OAuth token.

    Args:
        options: The OAuth token request options
        client: Optional client instance to use for the request
        throw_on_error: Whether to throw an exception on error

    Returns:
        The OAuth token response or error
    """
    response = await (client or default_client).get_async_httpx_client().post(
        url="/oauth/token",
        json=options.body or {},
        headers=options.headers or {},
    )
    if response.status_code >= 400:
        if throw_on_error:
            raise Exception(f"Failed to get OAuth token: {response.text}")
        return OauthTokenError(error=response.text)
    return OauthTokenResponse(**response.json())