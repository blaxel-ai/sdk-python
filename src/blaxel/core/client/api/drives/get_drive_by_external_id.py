from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.drive import Drive
from ...types import Response


def _get_kwargs(
    external_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/drives/by-external-id/{external_id}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, Drive] | None:
    if response.status_code == 200:
        response_200 = Drive.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Drive]]:
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
) -> Response[Union[Any, Drive]]:
    """Get drive by external ID

     Returns a drive matching the given external ID. If no drive is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Drive]]
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
) -> Union[Any, Drive] | None:
    """Get drive by external ID

     Returns a drive matching the given external ID. If no drive is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Drive]
    """

    return sync_detailed(
        external_id=external_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    external_id: str,
    *,
    client: Client,
) -> Response[Union[Any, Drive]]:
    """Get drive by external ID

     Returns a drive matching the given external ID. If no drive is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Drive]]
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
) -> Union[Any, Drive] | None:
    """Get drive by external ID

     Returns a drive matching the given external ID. If no drive is found, returns 404.

    Args:
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Drive]
    """

    return (
        await asyncio_detailed(
            external_id=external_id,
            client=client,
        )
    ).parsed
