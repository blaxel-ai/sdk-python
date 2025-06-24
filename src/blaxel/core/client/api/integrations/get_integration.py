from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.integration import Integration
from ...types import Response


def _get_kwargs(
    integration_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/integrations/{integration_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Integration]:
    if response.status_code == 200:
        response_200 = Integration.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Integration]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    integration_name: str,
    *,
    client: Union[Client],
) -> Response[Integration]:
    """List integrations connections

     Returns integration information by name.

    Args:
        integration_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Integration]
    """

    kwargs = _get_kwargs(
        integration_name=integration_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    integration_name: str,
    *,
    client: Union[Client],
) -> Optional[Integration]:
    """List integrations connections

     Returns integration information by name.

    Args:
        integration_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Integration
    """

    return sync_detailed(
        integration_name=integration_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    integration_name: str,
    *,
    client: Union[Client],
) -> Response[Integration]:
    """List integrations connections

     Returns integration information by name.

    Args:
        integration_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Integration]
    """

    kwargs = _get_kwargs(
        integration_name=integration_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    integration_name: str,
    *,
    client: Union[Client],
) -> Optional[Integration]:
    """List integrations connections

     Returns integration information by name.

    Args:
        integration_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Integration
    """

    return (
        await asyncio_detailed(
            integration_name=integration_name,
            client=client,
        )
    ).parsed
