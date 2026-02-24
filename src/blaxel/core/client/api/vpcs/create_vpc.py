from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.vpc import VPC
from ...types import Response


def _get_kwargs(
    *,
    body: VPC,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/vpcs",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> VPC | None:
    if response.status_code == 200:
        response_200 = VPC.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[VPC]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: VPC,
) -> Response[VPC]:
    """Create a VPC for the workspace

    Args:
        body (VPC): Virtual Private Cloud scoped to a workspace for network isolation and
            dedicated egress

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VPC]
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
    body: VPC,
) -> VPC | None:
    """Create a VPC for the workspace

    Args:
        body (VPC): Virtual Private Cloud scoped to a workspace for network isolation and
            dedicated egress

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VPC
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: VPC,
) -> Response[VPC]:
    """Create a VPC for the workspace

    Args:
        body (VPC): Virtual Private Cloud scoped to a workspace for network isolation and
            dedicated egress

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VPC]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: VPC,
) -> VPC | None:
    """Create a VPC for the workspace

    Args:
        body (VPC): Virtual Private Cloud scoped to a workspace for network isolation and
            dedicated egress

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VPC
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
