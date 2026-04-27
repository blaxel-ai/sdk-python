from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.image_share_target import ImageShareTarget
from ...types import Response


def _get_kwargs(
    resource_type: str,
    image_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/images/{resource_type}/{image_name}/share",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, list["ImageShareTarget"]] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ImageShareTarget.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, list["ImageShareTarget"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
) -> Response[Union[Any, list["ImageShareTarget"]]]:
    """List image shares

     Returns the list of workspaces that a container image is currently shared with.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['ImageShareTarget']]]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
) -> Union[Any, list["ImageShareTarget"]] | None:
    """List image shares

     Returns the list of workspaces that a container image is currently shared with.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['ImageShareTarget']]
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
) -> Response[Union[Any, list["ImageShareTarget"]]]:
    """List image shares

     Returns the list of workspaces that a container image is currently shared with.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['ImageShareTarget']]]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
) -> Union[Any, list["ImageShareTarget"]] | None:
    """List image shares

     Returns the list of workspaces that a container image is currently shared with.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['ImageShareTarget']]
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            client=client,
        )
    ).parsed
