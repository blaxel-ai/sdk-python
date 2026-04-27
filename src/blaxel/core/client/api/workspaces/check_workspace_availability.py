from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.check_workspace_availability_body import CheckWorkspaceAvailabilityBody
from ...models.workspace_availability import WorkspaceAvailability
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CheckWorkspaceAvailabilityBody,
    with_reason: Union[Unset, bool] = UNSET,
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
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union["WorkspaceAvailability", bool] | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["WorkspaceAvailability", bool]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = WorkspaceAvailability.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            return cast(Union["WorkspaceAvailability", bool], data)

        response_200 = _parse_response_200(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union["WorkspaceAvailability", bool]]:
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
    with_reason: Union[Unset, bool] = UNSET,
) -> Response[Union["WorkspaceAvailability", bool]]:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (Union[Unset, bool]):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['WorkspaceAvailability', bool]]
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
    with_reason: Union[Unset, bool] = UNSET,
) -> Union["WorkspaceAvailability", bool] | None:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (Union[Unset, bool]):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['WorkspaceAvailability', bool]
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
    with_reason: Union[Unset, bool] = UNSET,
) -> Response[Union["WorkspaceAvailability", bool]]:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (Union[Unset, bool]):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['WorkspaceAvailability', bool]]
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
    with_reason: Union[Unset, bool] = UNSET,
) -> Union["WorkspaceAvailability", bool] | None:
    """Check workspace availability

     Check if a workspace is available.

    Args:
        with_reason (Union[Unset, bool]):
        body (CheckWorkspaceAvailabilityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['WorkspaceAvailability', bool]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            with_reason=with_reason,
        )
    ).parsed
