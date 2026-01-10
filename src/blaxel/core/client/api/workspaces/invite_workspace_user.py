from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.invite_workspace_user_body import InviteWorkspaceUserBody
from ...models.pending_invitation import PendingInvitation
from ...types import Response


def _get_kwargs(
    *,
    body: InviteWorkspaceUserBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/users",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, PendingInvitation] | None:
    if response.status_code == 200:
        response_200 = PendingInvitation.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, PendingInvitation]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: InviteWorkspaceUserBody,
) -> Response[Union[Any, PendingInvitation]]:
    """Invite user to workspace

     Invites a new team member to the workspace by email. The invitee will receive an email to accept the
    invitation before gaining access to workspace resources.

    Args:
        body (InviteWorkspaceUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PendingInvitation]]
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
    body: InviteWorkspaceUserBody,
) -> Union[Any, PendingInvitation] | None:
    """Invite user to workspace

     Invites a new team member to the workspace by email. The invitee will receive an email to accept the
    invitation before gaining access to workspace resources.

    Args:
        body (InviteWorkspaceUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PendingInvitation]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: InviteWorkspaceUserBody,
) -> Response[Union[Any, PendingInvitation]]:
    """Invite user to workspace

     Invites a new team member to the workspace by email. The invitee will receive an email to accept the
    invitation before gaining access to workspace resources.

    Args:
        body (InviteWorkspaceUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PendingInvitation]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: InviteWorkspaceUserBody,
) -> Union[Any, PendingInvitation] | None:
    """Invite user to workspace

     Invites a new team member to the workspace by email. The invitee will receive an email to accept the
    invitation before gaining access to workspace resources.

    Args:
        body (InviteWorkspaceUserBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PendingInvitation]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
