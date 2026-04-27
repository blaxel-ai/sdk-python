from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.image import Image
from ...models.pending_image_share import PendingImageShare
from ...models.share_image_body import ShareImageBody
from ...types import Response


def _get_kwargs(
    resource_type: str,
    image_name: str,
    *,
    body: ShareImageBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/images/{resource_type}/{image_name}/share",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, Image, PendingImageShare] | None:
    if response.status_code == 200:
        response_200 = Image.from_dict(response.json())

        return response_200
    if response.status_code == 202:
        response_202 = PendingImageShare.from_dict(response.json())

        return response_202
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, Image, PendingImageShare]]:
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
    body: ShareImageBody,
) -> Response[Union[Any, Image, PendingImageShare]]:
    """Share a container image

     Shares a container image with another workspace by copying the metadata record. The underlying
    storage (S3) data is not duplicated. For same-account targets the share is applied immediately. For
    cross-account targets, a pending image share is created and must be explicitly accepted by an admin
    of the target workspace; the correct target account ID must be supplied as an anti-spam measure.

    Args:
        resource_type (str):
        image_name (str):
        body (ShareImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image, PendingImageShare]]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        body=body,
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
    body: ShareImageBody,
) -> Union[Any, Image, PendingImageShare] | None:
    """Share a container image

     Shares a container image with another workspace by copying the metadata record. The underlying
    storage (S3) data is not duplicated. For same-account targets the share is applied immediately. For
    cross-account targets, a pending image share is created and must be explicitly accepted by an admin
    of the target workspace; the correct target account ID must be supplied as an anti-spam measure.

    Args:
        resource_type (str):
        image_name (str):
        body (ShareImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image, PendingImageShare]
    """

    return sync_detailed(
        resource_type=resource_type,
        image_name=image_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    body: ShareImageBody,
) -> Response[Union[Any, Image, PendingImageShare]]:
    """Share a container image

     Shares a container image with another workspace by copying the metadata record. The underlying
    storage (S3) data is not duplicated. For same-account targets the share is applied immediately. For
    cross-account targets, a pending image share is created and must be explicitly accepted by an admin
    of the target workspace; the correct target account ID must be supplied as an anti-spam measure.

    Args:
        resource_type (str):
        image_name (str):
        body (ShareImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Image, PendingImageShare]]
    """

    kwargs = _get_kwargs(
        resource_type=resource_type,
        image_name=image_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    resource_type: str,
    image_name: str,
    *,
    client: Client,
    body: ShareImageBody,
) -> Union[Any, Image, PendingImageShare] | None:
    """Share a container image

     Shares a container image with another workspace by copying the metadata record. The underlying
    storage (S3) data is not duplicated. For same-account targets the share is applied immediately. For
    cross-account targets, a pending image share is created and must be explicitly accepted by an admin
    of the target workspace; the correct target account ID must be supplied as an anti-spam measure.

    Args:
        resource_type (str):
        image_name (str):
        body (ShareImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Image, PendingImageShare]
    """

    return (
        await asyncio_detailed(
            resource_type=resource_type,
            image_name=image_name,
            client=client,
            body=body,
        )
    ).parsed
