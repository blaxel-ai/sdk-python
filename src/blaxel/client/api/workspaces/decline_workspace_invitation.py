from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.pending_invitation import PendingInvitation
from ...types import Response


def _get_kwargs(
    workspace_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/workspaces/{workspace_name}/decline",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[PendingInvitation]:
    if response.status_code == 200:
        response_200 = PendingInvitation.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PendingInvitation]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_name: str,
    *,
    client: Union[Client],
) -> Response[PendingInvitation]:
    """Decline invitation to workspace

     Declines an invitation to a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PendingInvitation]
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
    client: Union[Client],
) -> Optional[PendingInvitation]:
    """Decline invitation to workspace

     Declines an invitation to a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PendingInvitation
    """

    return sync_detailed(
        workspace_name=workspace_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace_name: str,
    *,
    client: Union[Client],
) -> Response[PendingInvitation]:
    """Decline invitation to workspace

     Declines an invitation to a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PendingInvitation]
    """

    kwargs = _get_kwargs(
        workspace_name=workspace_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_name: str,
    *,
    client: Union[Client],
) -> Optional[PendingInvitation]:
    """Decline invitation to workspace

     Declines an invitation to a workspace.

    Args:
        workspace_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PendingInvitation
    """

    return (
        await asyncio_detailed(
            workspace_name=workspace_name,
            client=client,
        )
    ).parsed
