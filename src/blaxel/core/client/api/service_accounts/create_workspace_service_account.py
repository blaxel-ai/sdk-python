from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.create_workspace_service_account_body import CreateWorkspaceServiceAccountBody
from ...models.create_workspace_service_account_response_200 import (
    CreateWorkspaceServiceAccountResponse200,
)
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWorkspaceServiceAccountBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/service_accounts",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> CreateWorkspaceServiceAccountResponse200 | None:
    if response.status_code == 200:
        response_200 = CreateWorkspaceServiceAccountResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[CreateWorkspaceServiceAccountResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: CreateWorkspaceServiceAccountBody,
) -> Response[CreateWorkspaceServiceAccountResponse200]:
    """Create service account

     Creates a new service account for machine-to-machine authentication. Returns client ID and secret
    (secret is only shown once at creation). Use these credentials for OAuth client_credentials flow.

    Args:
        body (CreateWorkspaceServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateWorkspaceServiceAccountResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: CreateWorkspaceServiceAccountBody,
) -> CreateWorkspaceServiceAccountResponse200 | None:
    """Create service account

     Creates a new service account for machine-to-machine authentication. Returns client ID and secret
    (secret is only shown once at creation). Use these credentials for OAuth client_credentials flow.

    Args:
        body (CreateWorkspaceServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateWorkspaceServiceAccountResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: CreateWorkspaceServiceAccountBody,
) -> Response[CreateWorkspaceServiceAccountResponse200]:
    """Create service account

     Creates a new service account for machine-to-machine authentication. Returns client ID and secret
    (secret is only shown once at creation). Use these credentials for OAuth client_credentials flow.

    Args:
        body (CreateWorkspaceServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateWorkspaceServiceAccountResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: CreateWorkspaceServiceAccountBody,
) -> CreateWorkspaceServiceAccountResponse200 | None:
    """Create service account

     Creates a new service account for machine-to-machine authentication. Returns client ID and secret
    (secret is only shown once at creation). Use these credentials for OAuth client_credentials flow.

    Args:
        body (CreateWorkspaceServiceAccountBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateWorkspaceServiceAccountResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
