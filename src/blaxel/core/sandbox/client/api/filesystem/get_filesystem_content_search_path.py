from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.content_search_response import ContentSearchResponse
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    query: str,
    case_sensitive: bool | Unset = UNSET,
    max_results: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    context_lines: int | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    params["caseSensitive"] = case_sensitive

    params["maxResults"] = max_results

    params["filePattern"] = file_pattern

    params["excludeDirs"] = exclude_dirs

    params["contextLines"] = context_lines

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/filesystem-content-search/{path}".format(
            path=quote(str(path), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ContentSearchResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ContentSearchResponse.from_dict(response.json())

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
) -> Response[ContentSearchResponse | ErrorResponse]:
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
    query: str,
    case_sensitive: bool | Unset = UNSET,
    max_results: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    context_lines: int | Unset = UNSET,
) -> Response[ContentSearchResponse | ErrorResponse]:
    """Search for text content in files

     Searches for text content inside files. Returns each matching line, with the lines around it when
    contextLines is set.

    Args:
        path (str):
        query (str):
        case_sensitive (bool | Unset):
        max_results (int | Unset):
        file_pattern (str | Unset):
        exclude_dirs (str | Unset):
        context_lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContentSearchResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        path=path,
        query=query,
        case_sensitive=case_sensitive,
        max_results=max_results,
        file_pattern=file_pattern,
        exclude_dirs=exclude_dirs,
        context_lines=context_lines,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    query: str,
    case_sensitive: bool | Unset = UNSET,
    max_results: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    context_lines: int | Unset = UNSET,
) -> ContentSearchResponse | ErrorResponse | None:
    """Search for text content in files

     Searches for text content inside files. Returns each matching line, with the lines around it when
    contextLines is set.

    Args:
        path (str):
        query (str):
        case_sensitive (bool | Unset):
        max_results (int | Unset):
        file_pattern (str | Unset):
        exclude_dirs (str | Unset):
        context_lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContentSearchResponse | ErrorResponse
    """

    return sync_detailed(
        path=path,
        client=client,
        query=query,
        case_sensitive=case_sensitive,
        max_results=max_results,
        file_pattern=file_pattern,
        exclude_dirs=exclude_dirs,
        context_lines=context_lines,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    query: str,
    case_sensitive: bool | Unset = UNSET,
    max_results: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    context_lines: int | Unset = UNSET,
) -> Response[ContentSearchResponse | ErrorResponse]:
    """Search for text content in files

     Searches for text content inside files. Returns each matching line, with the lines around it when
    contextLines is set.

    Args:
        path (str):
        query (str):
        case_sensitive (bool | Unset):
        max_results (int | Unset):
        file_pattern (str | Unset):
        exclude_dirs (str | Unset):
        context_lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ContentSearchResponse | ErrorResponse]
    """

    kwargs = _get_kwargs(
        path=path,
        query=query,
        case_sensitive=case_sensitive,
        max_results=max_results,
        file_pattern=file_pattern,
        exclude_dirs=exclude_dirs,
        context_lines=context_lines,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    query: str,
    case_sensitive: bool | Unset = UNSET,
    max_results: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
    exclude_dirs: str | Unset = UNSET,
    context_lines: int | Unset = UNSET,
) -> ContentSearchResponse | ErrorResponse | None:
    """Search for text content in files

     Searches for text content inside files. Returns each matching line, with the lines around it when
    contextLines is set.

    Args:
        path (str):
        query (str):
        case_sensitive (bool | Unset):
        max_results (int | Unset):
        file_pattern (str | Unset):
        exclude_dirs (str | Unset):
        context_lines (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ContentSearchResponse | ErrorResponse
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            query=query,
            case_sensitive=case_sensitive,
            max_results=max_results,
            file_pattern=file_pattern,
            exclude_dirs=exclude_dirs,
            context_lines=context_lines,
        )
    ).parsed
