from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.create_drive_access_token_response_200 import CreateDriveAccessTokenResponse200
from ...types import Response


def _get_kwargs(
    drive_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/drives/{drive_name}/access-token",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, CreateDriveAccessTokenResponse200] | None:
    if response.status_code == 200:
        response_200 = CreateDriveAccessTokenResponse200.from_dict(response.json())

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, CreateDriveAccessTokenResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    drive_name: str,
    *,
    client: Client,
) -> Response[Union[Any, CreateDriveAccessTokenResponse200]]:
    """Create drive access token

     Issues a short-lived JWT access token scoped to a specific drive. The token can be used as Bearer
    authentication for direct S3 operations against the drive's SeaweedFS bucket.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateDriveAccessTokenResponse200]]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    drive_name: str,
    *,
    client: Client,
) -> Union[Any, CreateDriveAccessTokenResponse200] | None:
    """Create drive access token

     Issues a short-lived JWT access token scoped to a specific drive. The token can be used as Bearer
    authentication for direct S3 operations against the drive's SeaweedFS bucket.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateDriveAccessTokenResponse200]
    """

    return sync_detailed(
        drive_name=drive_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    drive_name: str,
    *,
    client: Client,
) -> Response[Union[Any, CreateDriveAccessTokenResponse200]]:
    """Create drive access token

     Issues a short-lived JWT access token scoped to a specific drive. The token can be used as Bearer
    authentication for direct S3 operations against the drive's SeaweedFS bucket.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateDriveAccessTokenResponse200]]
    """

    kwargs = _get_kwargs(
        drive_name=drive_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    drive_name: str,
    *,
    client: Client,
) -> Union[Any, CreateDriveAccessTokenResponse200] | None:
    """Create drive access token

     Issues a short-lived JWT access token scoped to a specific drive. The token can be used as Bearer
    authentication for direct S3 operations against the drive's SeaweedFS bucket.

    Args:
        drive_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateDriveAccessTokenResponse200]
    """

    return (
        await asyncio_detailed(
            drive_name=drive_name,
            client=client,
        )
    ).parsed
