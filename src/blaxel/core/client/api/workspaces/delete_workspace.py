from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.workspace import Workspace
from ...types import Response


def _get_kwargs(
    workspace_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/workspaces/{workspace_name}".format(
            workspace_name=quote(str(workspace_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | Workspace | None:
    if response.status_code == 200:
        response_200 = Workspace.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(errors.error_json(response))

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Error | Workspace]:
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
) -> Response[Error | Workspace]:
    """Delete workspace tenant

     Permanently deletes a workspace and ALL its resources (agents, functions, sandboxes, volumes, etc.).
    This action cannot be undone. Only workspace admins can delete a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Workspace]
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
) -> Error | Workspace | None:
    """Delete workspace tenant

     Permanently deletes a workspace and ALL its resources (agents, functions, sandboxes, volumes, etc.).
    This action cannot be undone. Only workspace admins can delete a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Workspace
    """

    return sync_detailed(
        workspace_name=workspace_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_name: str,
    *,
    client: Client,
) -> Response[Error | Workspace]:
    """Delete workspace tenant

     Permanently deletes a workspace and ALL its resources (agents, functions, sandboxes, volumes, etc.).
    This action cannot be undone. Only workspace admins can delete a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Workspace]
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
) -> Error | Workspace | None:
    """Delete workspace tenant

     Permanently deletes a workspace and ALL its resources (agents, functions, sandboxes, volumes, etc.).
    This action cannot be undone. Only workspace admins can delete a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Workspace
    """

    return (
        await asyncio_detailed(
            workspace_name=workspace_name,
            client=client,
        )
    ).parsed
