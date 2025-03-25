from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.update_workspace_user_role_body import UpdateWorkspaceUserRoleBody
from ...models.workspace_user import WorkspaceUser
from ...types import Response


def _get_kwargs(
    sub_or_email: str,
    *,
    body: UpdateWorkspaceUserRoleBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/users/{sub_or_email}",
    }

    if type(body) == dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, WorkspaceUser]]:
    if response.status_code == 200:
        response_200 = WorkspaceUser.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, WorkspaceUser]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sub_or_email: str,
    *,
    client: Union[Client],
    body: UpdateWorkspaceUserRoleBody,
) -> Response[Union[Any, WorkspaceUser]]:
    """Update user role in workspace

     Updates the role of a user in the workspace.

    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, WorkspaceUser]]
    """

    kwargs = _get_kwargs(
        sub_or_email=sub_or_email,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sub_or_email: str,
    *,
    client: Union[Client],
    body: UpdateWorkspaceUserRoleBody,
) -> Optional[Union[Any, WorkspaceUser]]:
    """Update user role in workspace

     Updates the role of a user in the workspace.

    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, WorkspaceUser]
    """

    return sync_detailed(
        sub_or_email=sub_or_email,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sub_or_email: str,
    *,
    client: Union[Client],
    body: UpdateWorkspaceUserRoleBody,
) -> Response[Union[Any, WorkspaceUser]]:
    """Update user role in workspace

     Updates the role of a user in the workspace.

    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, WorkspaceUser]]
    """

    kwargs = _get_kwargs(
        sub_or_email=sub_or_email,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sub_or_email: str,
    *,
    client: Union[Client],
    body: UpdateWorkspaceUserRoleBody,
) -> Optional[Union[Any, WorkspaceUser]]:
    """Update user role in workspace

     Updates the role of a user in the workspace.

    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, WorkspaceUser]
    """

    return (
        await asyncio_detailed(
            sub_or_email=sub_or_email,
            client=client,
            body=body,
        )
    ).parsed
