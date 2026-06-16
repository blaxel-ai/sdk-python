from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.sandbox_fork_request import SandboxForkRequest
from ...models.sandbox_fork_response import SandboxForkResponse
from ...types import Response


def _get_kwargs(
    sandbox_name: str,
    *,
    body: SandboxForkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_name}/fork",
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
) -> Union[Error, SandboxForkResponse] | None:
    if response.status_code == 200:
        response_200 = SandboxForkResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, SandboxForkResponse]]:
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
    body: SandboxForkRequest,
) -> Response[Union[Error, SandboxForkResponse]]:
    """Fork sandbox

     Forks a sandbox into a new sandbox or application. When forking to a sandbox, the target must not
    already exist (409 if it does). When forking to an application, a new revision is added if the app
    already exists, or a new application is created. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxForkResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Union[Error, SandboxForkResponse] | None:
    """Fork sandbox

     Forks a sandbox into a new sandbox or application. When forking to a sandbox, the target must not
    already exist (409 if it does). When forking to an application, a new revision is added if the app
    already exists, or a new application is created. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxForkResponse]
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Response[Union[Error, SandboxForkResponse]]:
    """Fork sandbox

     Forks a sandbox into a new sandbox or application. When forking to a sandbox, the target must not
    already exist (409 if it does). When forking to an application, a new revision is added if the app
    already exists, or a new application is created. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SandboxForkResponse]]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    body: SandboxForkRequest,
) -> Union[Error, SandboxForkResponse] | None:
    """Fork sandbox

     Forks a sandbox into a new sandbox or application. When forking to a sandbox, the target must not
    already exist (409 if it does). When forking to an application, a new revision is added if the app
    already exists, or a new application is created. This is a WIP endpoint — the full implementation
    depends on the execution plane.

    Args:
        sandbox_name (str):
        body (SandboxForkRequest): Request body for forking a sandbox into an application. Creates
            a new application or adds a canary revision to an existing one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SandboxForkResponse]
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
        )
    ).parsed
