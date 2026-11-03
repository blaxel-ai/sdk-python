from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.workspace import Workspace
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace_name: str,
    *,
    count_resources: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["countResources"] = count_resources

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workspaces/{workspace_name}".format(
            workspace_name=quote(str(workspace_name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | Workspace | None:
    if response.status_code == 200:
        response_200 = Workspace.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

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
    count_resources: bool | Unset = False,
) -> Response[Error | Workspace]:
    """Get workspace details

     Returns detailed information about a workspace including its display name, account ID, status, and
    runtime configuration.

    Args:
        workspace_name (str):
        count_resources (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_name=workspace_name,
        count_resources=count_resources,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_name: str,
    *,
    client: Client,
    count_resources: bool | Unset = False,
) -> Error | Workspace | None:
    """Get workspace details

     Returns detailed information about a workspace including its display name, account ID, status, and
    runtime configuration.

    Args:
        workspace_name (str):
        count_resources (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Workspace
    """

    return sync_detailed(
        workspace_name=workspace_name,
        client=client,
        count_resources=count_resources,
    ).parsed


async def asyncio_detailed(
    workspace_name: str,
    *,
    client: Client,
    count_resources: bool | Unset = False,
) -> Response[Error | Workspace]:
    """Get workspace details

     Returns detailed information about a workspace including its display name, account ID, status, and
    runtime configuration.

    Args:
        workspace_name (str):
        count_resources (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Workspace]
    """

    kwargs = _get_kwargs(
        workspace_name=workspace_name,
        count_resources=count_resources,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_name: str,
    *,
    client: Client,
    count_resources: bool | Unset = False,
) -> Error | Workspace | None:
    """Get workspace details

     Returns detailed information about a workspace including its display name, account ID, status, and
    runtime configuration.

    Args:
        workspace_name (str):
        count_resources (bool | Unset):  Default: False.

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
            count_resources=count_resources,
        )
    ).parsed
