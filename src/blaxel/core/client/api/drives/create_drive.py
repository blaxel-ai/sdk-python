from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.drive import Drive
from ...types import Response


def _get_kwargs(
    *,
    body: Drive,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/drives",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, Drive] | None:
    if response.status_code == 200:
        response_200 = Drive.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
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
    *,
    client: Client,
    body: Drive,
) -> Response[Union[Any, Drive]]:
    """Create a drive

     Creates a new drive in the workspace. Drives are backed by SeaweedFS buckets and can be mounted at
    runtime to sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives are backed by SeaweedFS buckets and can be mounted at
            runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Drive]]
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
    body: Drive,
) -> Union[Any, Drive] | None:
    """Create a drive

     Creates a new drive in the workspace. Drives are backed by SeaweedFS buckets and can be mounted at
    runtime to sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives are backed by SeaweedFS buckets and can be mounted at
            runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Drive]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: Drive,
) -> Response[Union[Any, Drive]]:
    """Create a drive

     Creates a new drive in the workspace. Drives are backed by SeaweedFS buckets and can be mounted at
    runtime to sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives are backed by SeaweedFS buckets and can be mounted at
            runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Drive]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: Drive,
) -> Union[Any, Drive] | None:
    """Create a drive

     Creates a new drive in the workspace. Drives are backed by SeaweedFS buckets and can be mounted at
    runtime to sandboxes.

    Args:
        body (Drive): Drive providing persistent storage that can be attached to agents,
            functions, and sandboxes. Drives are backed by SeaweedFS buckets and can be mounted at
            runtime via the sbx API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Drive]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
