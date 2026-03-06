from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.test_feature_flag_response_200 import TestFeatureFlagResponse200
from ...types import Response


def _get_kwargs(
    feature_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/features/{feature_key}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, TestFeatureFlagResponse200] | None:
    if response.status_code == 200:
        response_200 = TestFeatureFlagResponse200.from_dict(response.json())

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
) -> Response[Union[Error, TestFeatureFlagResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    feature_key: str,
    *,
    client: Client,
) -> Response[Union[Error, TestFeatureFlagResponse200]]:
    """Retrieve feature flag evaluation for workspace

     Evaluates a specific feature flag for the workspace with full details including variant and payload.
    Useful for testing and debugging feature flag targeting.

    Args:
        feature_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TestFeatureFlagResponse200]]
    """

    kwargs = _get_kwargs(
        feature_key=feature_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    feature_key: str,
    *,
    client: Client,
) -> Union[Error, TestFeatureFlagResponse200] | None:
    """Retrieve feature flag evaluation for workspace

     Evaluates a specific feature flag for the workspace with full details including variant and payload.
    Useful for testing and debugging feature flag targeting.

    Args:
        feature_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TestFeatureFlagResponse200]
    """

    return sync_detailed(
        feature_key=feature_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    feature_key: str,
    *,
    client: Client,
) -> Response[Union[Error, TestFeatureFlagResponse200]]:
    """Retrieve feature flag evaluation for workspace

     Evaluates a specific feature flag for the workspace with full details including variant and payload.
    Useful for testing and debugging feature flag targeting.

    Args:
        feature_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, TestFeatureFlagResponse200]]
    """

    kwargs = _get_kwargs(
        feature_key=feature_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    feature_key: str,
    *,
    client: Client,
) -> Union[Error, TestFeatureFlagResponse200] | None:
    """Retrieve feature flag evaluation for workspace

     Evaluates a specific feature flag for the workspace with full details including variant and payload.
    Useful for testing and debugging feature flag targeting.

    Args:
        feature_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, TestFeatureFlagResponse200]
    """

    return (
        await asyncio_detailed(
            feature_key=feature_key,
            client=client,
        )
    ).parsed
