from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.image import Image
from ...types import Response


def _get_kwargs(
    resource_type: str,
    image_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/images/{resource_type}/{image_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, Image] | None:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Image]]:
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
) -> Response[Union[Any, Image]]:
    """Delete container image

     Deletes a container image and all its tags from the workspace registry. Will fail if the image is
    currently in use by an active deployment.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image]]
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
) -> Union[Any, Image] | None:
    """Delete container image

     Deletes a container image and all its tags from the workspace registry. Will fail if the image is
    currently in use by an active deployment.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image]
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
) -> Response[Union[Any, Image]]:
    """Delete container image

     Deletes a container image and all its tags from the workspace registry. Will fail if the image is
    currently in use by an active deployment.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image]]
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
) -> Union[Any, Image] | None:
    """Delete container image

     Deletes a container image and all its tags from the workspace registry. Will fail if the image is
    currently in use by an active deployment.

    Args:
        resource_type (str):
        image_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image]
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            client=client,
        )
    ).parsed
