from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox import Sandbox
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_name: str,
    *,
    show_secrets: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["show_secrets"] = show_secrets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_name}",
        "params": params,
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
    sandbox_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Union[Error, Sandbox]]:
    """Get sandbox

     Returns detailed information about a sandbox including its configuration, attached volumes,
    lifecycle policies, and API endpoint URL.

    Args:
        sandbox_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        show_secrets=show_secrets,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Union[Error, Sandbox] | None:
    """Get sandbox

     Returns detailed information about a sandbox including its configuration, attached volumes,
    lifecycle policies, and API endpoint URL.

    Args:
        sandbox_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        show_secrets=show_secrets,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Union[Error, Sandbox]]:
    """Get sandbox

     Returns detailed information about a sandbox including its configuration, attached volumes,
    lifecycle policies, and API endpoint URL.

    Args:
        sandbox_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Sandbox]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        show_secrets=show_secrets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    show_secrets: Union[Unset, bool] = UNSET,
) -> Union[Error, Sandbox] | None:
    """Get sandbox

     Returns detailed information about a sandbox including its configuration, attached volumes,
    lifecycle policies, and API endpoint URL.

    Args:
        sandbox_name (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Sandbox]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            show_secrets=show_secrets,
        )
    ).parsed
