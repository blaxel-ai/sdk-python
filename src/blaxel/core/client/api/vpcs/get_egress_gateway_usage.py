from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.egress_gateway_usage import EgressGatewayUsage
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/egressgateways/usage",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> EgressGatewayUsage | None:
    if response.status_code == 200:
        response_200 = EgressGatewayUsage.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[EgressGatewayUsage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[EgressGatewayUsage]:
    """Egress gateway sandbox attachments

     Returns the inverse map (gateway → sandbox names) for the workspace. Used by the egress-IPs UI to
    render attachment counts without fetching the sandboxes listing full client-side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EgressGatewayUsage]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> EgressGatewayUsage | None:
    """Egress gateway sandbox attachments

     Returns the inverse map (gateway → sandbox names) for the workspace. Used by the egress-IPs UI to
    render attachment counts without fetching the sandboxes listing full client-side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EgressGatewayUsage
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[EgressGatewayUsage]:
    """Egress gateway sandbox attachments

     Returns the inverse map (gateway → sandbox names) for the workspace. Used by the egress-IPs UI to
    render attachment counts without fetching the sandboxes listing full client-side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EgressGatewayUsage]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> EgressGatewayUsage | None:
    """Egress gateway sandbox attachments

     Returns the inverse map (gateway → sandbox names) for the workspace. Used by the egress-IPs UI to
    render attachment counts without fetching the sandboxes listing full client-side.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EgressGatewayUsage
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
