from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.egress_ip import EgressIP
from ...types import Response


def _get_kwargs(
    vpc_name: str,
    gateway_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/vpcs/{vpc_name}/egressgateways/{gateway_name}/ips",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> list["EgressIP"] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EgressIP.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[list["EgressIP"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vpc_name: str,
    gateway_name: str,
    *,
    client: Client,
) -> Response[list["EgressIP"]]:
    """List egress IPs in a gateway

    Args:
        vpc_name (str):
        gateway_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['EgressIP']]
    """

    kwargs = _get_kwargs(
        vpc_name=vpc_name,
        gateway_name=gateway_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vpc_name: str,
    gateway_name: str,
    *,
    client: Client,
) -> list["EgressIP"] | None:
    """List egress IPs in a gateway

    Args:
        vpc_name (str):
        gateway_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EgressIP']
    """

    return sync_detailed(
        vpc_name=vpc_name,
        gateway_name=gateway_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    vpc_name: str,
    gateway_name: str,
    *,
    client: Client,
) -> Response[list["EgressIP"]]:
    """List egress IPs in a gateway

    Args:
        vpc_name (str):
        gateway_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['EgressIP']]
    """

    kwargs = _get_kwargs(
        vpc_name=vpc_name,
        gateway_name=gateway_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vpc_name: str,
    gateway_name: str,
    *,
    client: Client,
) -> list["EgressIP"] | None:
    """List egress IPs in a gateway

    Args:
        vpc_name (str):
        gateway_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EgressIP']
    """

    return (
        await asyncio_detailed(
            vpc_name=vpc_name,
            gateway_name=gateway_name,
            client=client,
        )
    ).parsed
