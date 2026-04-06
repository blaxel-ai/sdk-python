from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.create_image_body import CreateImageBody
from ...models.create_image_response_200 import CreateImageResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: CreateImageBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/images",
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
) -> Union[Any, CreateImageResponse200] | None:
    if response.status_code == 200:
        response_200 = CreateImageResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, CreateImageResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: CreateImageBody,
) -> Response[Union[Any, CreateImageResponse200]]:
    """Build a container image

     Builds a container image without creating a deployment. Returns a presigned URL for uploading source
    code. After upload, the image will be built and stored in the registry, but no agent, function,
    sandbox, or job will be created or updated.

    Args:
        body (CreateImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateImageResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: CreateImageBody,
) -> Union[Any, CreateImageResponse200] | None:
    """Build a container image

     Builds a container image without creating a deployment. Returns a presigned URL for uploading source
    code. After upload, the image will be built and stored in the registry, but no agent, function,
    sandbox, or job will be created or updated.

    Args:
        body (CreateImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateImageResponse200]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: CreateImageBody,
) -> Response[Union[Any, CreateImageResponse200]]:
    """Build a container image

     Builds a container image without creating a deployment. Returns a presigned URL for uploading source
    code. After upload, the image will be built and stored in the registry, but no agent, function,
    sandbox, or job will be created or updated.

    Args:
        body (CreateImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateImageResponse200]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: CreateImageBody,
) -> Union[Any, CreateImageResponse200] | None:
    """Build a container image

     Builds a container image without creating a deployment. Returns a presigned URL for uploading source
    code. After upload, the image will be built and stored in the registry, but no agent, function,
    sandbox, or job will be created or updated.

    Args:
        body (CreateImageBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateImageResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
