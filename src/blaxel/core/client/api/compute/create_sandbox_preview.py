from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.preview import Preview
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_name: str,
    *,
    body: Preview,
    force: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_name}/previews",
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


def _parse_response(*, client: Client, response: httpx.Response) -> Preview | None:
    if response.status_code == 200:
        response_200 = Preview.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Preview]:
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
    body: Preview,
    force: Union[Unset, bool] = UNSET,
) -> Response[Preview]:
    """Create Sandbox Preview

     Create a preview

    Args:
        sandbox_name (str):
        force (Union[Unset, bool]):
        body (Preview): Preview of a Resource

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Preview]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
        force=force,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_name: str,
    *,
    client: Client,
    body: Preview,
    force: Union[Unset, bool] = UNSET,
) -> Preview | None:
    """Create Sandbox Preview

     Create a preview

    Args:
        sandbox_name (str):
        force (Union[Unset, bool]):
        body (Preview): Preview of a Resource

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Preview
    """

    return sync_detailed(
        sandbox_name=sandbox_name,
        client=client,
        body=body,
        force=force,
    ).parsed


async def asyncio_detailed(
    sandbox_name: str,
    *,
    client: Client,
    body: Preview,
    force: Union[Unset, bool] = UNSET,
) -> Response[Preview]:
    """Create Sandbox Preview

     Create a preview

    Args:
        sandbox_name (str):
        force (Union[Unset, bool]):
        body (Preview): Preview of a Resource

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Preview]
    """

    kwargs = _get_kwargs(
        sandbox_name=sandbox_name,
        body=body,
        force=force,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_name: str,
    *,
    client: Client,
    body: Preview,
    force: Union[Unset, bool] = UNSET,
) -> Preview | None:
    """Create Sandbox Preview

     Create a preview

    Args:
        sandbox_name (str):
        force (Union[Unset, bool]):
        body (Preview): Preview of a Resource

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Preview
    """

    return (
        await asyncio_detailed(
            sandbox_name=sandbox_name,
            client=client,
            body=body,
            force=force,
        )
    ).parsed
