from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.egress_gateway import EgressGateway
from ...types import Response


def _get_kwargs(
    vpc_name: str,
    *,
    body: EgressGateway,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/vpcs/{vpc_name}/egressgateways",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> EgressGateway | None:
    if response.status_code == 200:
        response_200 = EgressGateway.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[EgressGateway]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vpc_name: str,
    *,
    client: Client,
    body: EgressGateway,
) -> Response[EgressGateway]:
    """Create an egress gateway in a VPC

    Args:
        vpc_name (str):
        body (EgressGateway): An egress gateway that manages outbound traffic routing within a
            VPC. Multiple egress IPs can be allocated from a single gateway.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EgressGateway]
    """

    kwargs = _get_kwargs(
        vpc_name=vpc_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vpc_name: str,
    *,
    client: Client,
    body: EgressGateway,
) -> EgressGateway | None:
    """Create an egress gateway in a VPC

    Args:
        vpc_name (str):
        body (EgressGateway): An egress gateway that manages outbound traffic routing within a
            VPC. Multiple egress IPs can be allocated from a single gateway.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EgressGateway
    """

    return sync_detailed(
        vpc_name=vpc_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    vpc_name: str,
    *,
    client: Client,
    body: EgressGateway,
) -> Response[EgressGateway]:
    """Create an egress gateway in a VPC

    Args:
        vpc_name (str):
        body (EgressGateway): An egress gateway that manages outbound traffic routing within a
            VPC. Multiple egress IPs can be allocated from a single gateway.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EgressGateway]
    """

    kwargs = _get_kwargs(
        vpc_name=vpc_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vpc_name: str,
    *,
    client: Client,
    body: EgressGateway,
) -> EgressGateway | None:
    """Create an egress gateway in a VPC

    Args:
        vpc_name (str):
        body (EgressGateway): An egress gateway that manages outbound traffic routing within a
            VPC. Multiple egress IPs can be allocated from a single gateway.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EgressGateway
    """

    return (
        await asyncio_detailed(
            vpc_name=vpc_name,
            client=client,
            body=body,
        )
    ).parsed
