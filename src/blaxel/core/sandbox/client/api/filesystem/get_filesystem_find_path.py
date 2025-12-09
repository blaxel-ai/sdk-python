from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.find_response import FindResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    type_: Union[Unset, str] = UNSET,
    patterns: Union[Unset, str] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    exclude_dirs: Union[Unset, str] = UNSET,
    exclude_hidden: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["type"] = type_

    params["patterns"] = patterns

    params["maxResults"] = max_results

    params["excludeDirs"] = exclude_dirs

    params["excludeHidden"] = exclude_hidden

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/filesystem-find/{path}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, FindResponse] | None:
    if response.status_code == 200:
        response_200 = FindResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, FindResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
    type_: Union[Unset, str] = UNSET,
    patterns: Union[Unset, str] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    exclude_dirs: Union[Unset, str] = UNSET,
    exclude_hidden: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, FindResponse]]:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (Union[Unset, str]):
        patterns (Union[Unset, str]):
        max_results (Union[Unset, int]):
        exclude_dirs (Union[Unset, str]):
        exclude_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, FindResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        type_=type_,
        patterns=patterns,
        max_results=max_results,
        exclude_dirs=exclude_dirs,
        exclude_hidden=exclude_hidden,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    type_: Union[Unset, str] = UNSET,
    patterns: Union[Unset, str] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    exclude_dirs: Union[Unset, str] = UNSET,
    exclude_hidden: Union[Unset, bool] = UNSET,
) -> Union[ErrorResponse, FindResponse] | None:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (Union[Unset, str]):
        patterns (Union[Unset, str]):
        max_results (Union[Unset, int]):
        exclude_dirs (Union[Unset, str]):
        exclude_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, FindResponse]
    """

    return sync_detailed(
        path=path,
        client=client,
        type_=type_,
        patterns=patterns,
        max_results=max_results,
        exclude_dirs=exclude_dirs,
        exclude_hidden=exclude_hidden,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    type_: Union[Unset, str] = UNSET,
    patterns: Union[Unset, str] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    exclude_dirs: Union[Unset, str] = UNSET,
    exclude_hidden: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, FindResponse]]:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (Union[Unset, str]):
        patterns (Union[Unset, str]):
        max_results (Union[Unset, int]):
        exclude_dirs (Union[Unset, str]):
        exclude_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, FindResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        type_=type_,
        patterns=patterns,
        max_results=max_results,
        exclude_dirs=exclude_dirs,
        exclude_hidden=exclude_hidden,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    type_: Union[Unset, str] = UNSET,
    patterns: Union[Unset, str] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    exclude_dirs: Union[Unset, str] = UNSET,
    exclude_hidden: Union[Unset, bool] = UNSET,
) -> Union[ErrorResponse, FindResponse] | None:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (Union[Unset, str]):
        patterns (Union[Unset, str]):
        max_results (Union[Unset, int]):
        exclude_dirs (Union[Unset, str]):
        exclude_hidden (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, FindResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            type_=type_,
            patterns=patterns,
            max_results=max_results,
            exclude_dirs=exclude_dirs,
            exclude_hidden=exclude_hidden,
        )
    ).parsed
