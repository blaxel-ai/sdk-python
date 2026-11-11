from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.find_response import FindResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    type_: str | Unset = UNSET,
    patterns: str | Unset = UNSET,
    max_results: int | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    exclude_hidden: bool | Unset = UNSET,
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
        "url": "/filesystem-find/{path}".format(
            path=quote(str(path), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ErrorResponse | FindResponse | None:
    if response.status_code == 200:
        response_200 = FindResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_422, response)
        return response_422

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(errors.error_json(response))

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ErrorResponse | FindResponse]:
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
    type_: str | Unset = UNSET,
    patterns: str | Unset = UNSET,
    max_results: int | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    exclude_hidden: bool | Unset = UNSET,
) -> Response[ErrorResponse | FindResponse]:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (str | Unset):
        patterns (str | Unset):
        max_results (int | Unset):
        exclude_dirs (str | Unset):
        exclude_hidden (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FindResponse]
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
    type_: str | Unset = UNSET,
    patterns: str | Unset = UNSET,
    max_results: int | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    exclude_hidden: bool | Unset = UNSET,
) -> ErrorResponse | FindResponse | None:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (str | Unset):
        patterns (str | Unset):
        max_results (int | Unset):
        exclude_dirs (str | Unset):
        exclude_hidden (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FindResponse
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
    type_: str | Unset = UNSET,
    patterns: str | Unset = UNSET,
    max_results: int | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    exclude_hidden: bool | Unset = UNSET,
) -> Response[ErrorResponse | FindResponse]:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (str | Unset):
        patterns (str | Unset):
        max_results (int | Unset):
        exclude_dirs (str | Unset):
        exclude_hidden (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | FindResponse]
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
    type_: str | Unset = UNSET,
    patterns: str | Unset = UNSET,
    max_results: int | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    exclude_hidden: bool | Unset = UNSET,
) -> ErrorResponse | FindResponse | None:
    """Find files and directories

     Finds files and directories using the find command.

    Args:
        path (str):
        type_ (str | Unset):
        patterns (str | Unset):
        max_results (int | Unset):
        exclude_dirs (str | Unset):
        exclude_hidden (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | FindResponse
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
