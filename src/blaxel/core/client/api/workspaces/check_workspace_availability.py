from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import Client
from ...models.check_workspace_availability_body import CheckWorkspaceAvailabilityBody
from ...models.workspace_availability import WorkspaceAvailability
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["withReason"] = with_reason

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workspaces/availability",
        "params": params,
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> bool | WorkspaceAvailability | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> bool | WorkspaceAvailability:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = WorkspaceAvailability.from_dict(data)

                return response_200_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(bool | WorkspaceAvailability, data)

        response_200 = _parse_response_200(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[bool | WorkspaceAvailability]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: bool | Unset = UNSET,
) -> Response[bool | WorkspaceAvailability]:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (bool | Unset):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool | WorkspaceAvailability]
    """

    kwargs = _get_kwargs(
        body=body,
        with_reason=with_reason,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: bool | Unset = UNSET,
) -> bool | WorkspaceAvailability | None:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (bool | Unset):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool | WorkspaceAvailability
    """

    return sync_detailed(
        client=client,
        body=body,
        with_reason=with_reason,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: bool | Unset = UNSET,
) -> Response[bool | WorkspaceAvailability]:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (bool | Unset):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool | WorkspaceAvailability]
    """

    kwargs = _get_kwargs(
        body=body,
        with_reason=with_reason,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: bool | Unset = UNSET,
) -> bool | WorkspaceAvailability | None:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (bool | Unset):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool | WorkspaceAvailability
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            with_reason=with_reason,
        )
    ).parsed
