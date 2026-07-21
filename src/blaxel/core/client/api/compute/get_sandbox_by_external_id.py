from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox import Sandbox
from ...types import Response


def _get_kwargs(
    external_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/by-external-id/{external_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Error, Sandbox] | None:
    if response.status_code == 200:
        response_200 = Sandbox.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Error, Sandbox]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    external_id: str,
    *,
    client: Client,
) -> Response[Union[Error, Sandbox]]:
    """Get sandbox by external ID

     Returns the most recent non-terminated sandbox matching the given external ID. If no active sandbox
    is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
    """

    kwargs = _get_kwargs(
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    external_id: str,
    *,
    client: Client,
) -> Union[Error, Sandbox] | None:
    """Get sandbox by external ID

     Returns the most recent non-terminated sandbox matching the given external ID. If no active sandbox
    is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
    """

    return sync_detailed(
        external_id=external_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    external_id: str,
    *,
    client: Client,
) -> Response[Union[Error, Sandbox]]:
    """Get sandbox by external ID

     Returns the most recent non-terminated sandbox matching the given external ID. If no active sandbox
    is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
    """

    kwargs = _get_kwargs(
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    external_id: str,
    *,
    client: Client,
) -> Union[Error, Sandbox] | None:
    """Get sandbox by external ID

     Returns the most recent non-terminated sandbox matching the given external ID. If no active sandbox
    is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
    """

    return (
        await asyncio_detailed(
            external_id=external_id,
            client=client,
        )
    ).parsed
