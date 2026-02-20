from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.get_workspace_features_response_200 import GetWorkspaceFeaturesResponse200
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/features",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, GetWorkspaceFeaturesResponse200] | None:
    if response.status_code == 200:
        response_200 = GetWorkspaceFeaturesResponse200.from_dict(response.json())

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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, GetWorkspaceFeaturesResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[Error, GetWorkspaceFeaturesResponse200]]:
    """Get enabled features for workspace

     Returns only the feature flags that are currently enabled for the specified workspace. Disabled
    features are not included to prevent information leakage.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetWorkspaceFeaturesResponse200]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
) -> Union[Error, GetWorkspaceFeaturesResponse200] | None:
    """Get enabled features for workspace

     Returns only the feature flags that are currently enabled for the specified workspace. Disabled
    features are not included to prevent information leakage.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetWorkspaceFeaturesResponse200]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[Error, GetWorkspaceFeaturesResponse200]]:
    """Get enabled features for workspace

     Returns only the feature flags that are currently enabled for the specified workspace. Disabled
    features are not included to prevent information leakage.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetWorkspaceFeaturesResponse200]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
) -> Union[Error, GetWorkspaceFeaturesResponse200] | None:
    """Get enabled features for workspace

     Returns only the feature flags that are currently enabled for the specified workspace. Disabled
    features are not included to prevent information leakage.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetWorkspaceFeaturesResponse200]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
