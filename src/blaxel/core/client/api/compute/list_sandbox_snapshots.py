from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_snapshot import SandboxSnapshot
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sandboxes/{sandbox_name}/snapshots",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, list["SandboxSnapshot"]] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_sandbox_snapshots_item_data in _response_200:
            componentsschemas_sandbox_snapshots_item = SandboxSnapshot.from_dict(
                componentsschemas_sandbox_snapshots_item_data
            )

            response_200.append(componentsschemas_sandbox_snapshots_item)

        return response_200
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, list["SandboxSnapshot"]]]:
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
) -> Response[Union[Error, list["SandboxSnapshot"]]]:
    """List sandbox snapshots

     Returns a list of snapshots for the specified sandbox.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxSnapshot']]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
) -> Union[Error, list["SandboxSnapshot"]] | None:
    """List sandbox snapshots

     Returns a list of snapshots for the specified sandbox.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxSnapshot']]
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
) -> Response[Union[Error, list["SandboxSnapshot"]]]:
    """List sandbox snapshots

     Returns a list of snapshots for the specified sandbox.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['SandboxSnapshot']]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
) -> Union[Error, list["SandboxSnapshot"]] | None:
    """List sandbox snapshots

     Returns a list of snapshots for the specified sandbox.

    Args:
        sandbox_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['SandboxSnapshot']]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
        )
    ).parsed
