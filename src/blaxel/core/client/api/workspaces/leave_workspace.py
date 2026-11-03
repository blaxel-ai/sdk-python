from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.workspace import Workspace
from ...types import Response


def _get_kwargs(
    workspace_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/workspaces/{workspace_name}/leave".format(
            workspace_name=quote(str(workspace_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | Workspace | None:
    if response.status_code == 200:
        response_200 = Workspace.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        errors.retain_response(response_404, response)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | Workspace]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_name: str,
    *,
    client: Client,
) -> Response[Any | Workspace]:
    """Leave workspace

     Leaves a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_name=workspace_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_name: str,
    *,
    client: Client,
) -> Any | Workspace | None:
    """Leave workspace

     Leaves a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Workspace
    """

    return sync_detailed(
        workspace_name=workspace_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_name: str,
    *,
    client: Client,
) -> Response[Any | Workspace]:
    """Leave workspace

     Leaves a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_name=workspace_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_name: str,
    *,
    client: Client,
) -> Any | Workspace | None:
    """Leave workspace

     Leaves a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Workspace
    """

    return (
        await asyncio_detailed(
            workspace_name=workspace_name,
            client=client,
        )
    ).parsed
