from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.api_key import ApiKey
from ...models.create_api_key_for_service_account_body import CreateApiKeyForServiceAccountBody
from ...types import Response


def _get_kwargs(
    client_id: str,
    *,
    body: CreateApiKeyForServiceAccountBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/service_accounts/{client_id}/api_keys",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[ApiKey]:
    if response.status_code == 200:
        response_200 = ApiKey.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[ApiKey]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    client_id: str,
    *,
    client: Union[Client],
    body: CreateApiKeyForServiceAccountBody,
) -> Response[ApiKey]:
    """Create API key for service account

     Creates an API key for a service account.

    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKey]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    client_id: str,
    *,
    client: Union[Client],
    body: CreateApiKeyForServiceAccountBody,
) -> Optional[ApiKey]:
    """Create API key for service account

     Creates an API key for a service account.

    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKey
    """

    return sync_detailed(
        client_id=client_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    client_id: str,
    *,
    client: Union[Client],
    body: CreateApiKeyForServiceAccountBody,
) -> Response[ApiKey]:
    """Create API key for service account

     Creates an API key for a service account.

    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKey]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    client_id: str,
    *,
    client: Union[Client],
    body: CreateApiKeyForServiceAccountBody,
) -> Optional[ApiKey]:
    """Create API key for service account

     Creates an API key for a service account.

    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKey
    """

    return (
        await asyncio_detailed(
            client_id=client_id,
            client=client,
            body=body,
        )
    ).parsed
