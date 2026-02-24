from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.public_ips import PublicIps
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    region: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["region"] = region

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/publicIps",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> PublicIps | None:
    if response.status_code == 200:
        response_200 = PublicIps.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PublicIps]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    region: Union[Unset, str] = UNSET,
) -> Response[PublicIps]:
    """List public ips

     Returns a list of all public ips used in Blaxel..

    Args:
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublicIps]
    """

    kwargs = _get_kwargs(
        region=region,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    region: Union[Unset, str] = UNSET,
) -> PublicIps | None:
    """List public ips

     Returns a list of all public ips used in Blaxel..

    Args:
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublicIps
    """

    return sync_detailed(
        client=client,
        region=region,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    region: Union[Unset, str] = UNSET,
) -> Response[PublicIps]:
    """List public ips

     Returns a list of all public ips used in Blaxel..

    Args:
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PublicIps]
    """

    kwargs = _get_kwargs(
        region=region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    region: Union[Unset, str] = UNSET,
) -> PublicIps | None:
    """List public ips

     Returns a list of all public ips used in Blaxel..

    Args:
        region (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PublicIps
    """

    return (
        await asyncio_detailed(
            client=client,
            region=region,
        )
    ).parsed
