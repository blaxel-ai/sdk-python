from http import HTTPStatus
from io import BytesIO
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.directory import Directory
from ...models.error_response import ErrorResponse
from ...models.file_with_content import FileWithContent
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    path: str,
    *,
    download: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["download"] = download

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/filesystem/{path}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, Union["Directory", "FileWithContent", File]] | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["Directory", "FileWithContent", File]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = Directory.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = FileWithContent.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, bytes):
                raise TypeError()
            response_200_type_2 = File(payload=BytesIO(data))

            return response_200_type_2

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
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
) -> Response[Union[ErrorResponse, Union["Directory", "FileWithContent", File]]]:
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
    download: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, Union["Directory", "FileWithContent", File]]]:
    """Get file or directory information

     Get content of a file or listing of a directory. Use Accept header to control response format for
    files.

    Args:
        path (str):
        download (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['Directory', 'FileWithContent', File]]]
    """

    kwargs = _get_kwargs(
        path=path,
        download=download,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    download: Union[Unset, bool] = UNSET,
) -> Union[ErrorResponse, Union["Directory", "FileWithContent", File]] | None:
    """Get file or directory information

     Get content of a file or listing of a directory. Use Accept header to control response format for
    files.

    Args:
        path (str):
        download (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['Directory', 'FileWithContent', File]]
    """

    return sync_detailed(
        path=path,
        client=client,
        download=download,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    download: Union[Unset, bool] = UNSET,
) -> Response[Union[ErrorResponse, Union["Directory", "FileWithContent", File]]]:
    """Get file or directory information

     Get content of a file or listing of a directory. Use Accept header to control response format for
    files.

    Args:
        path (str):
        download (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, Union['Directory', 'FileWithContent', File]]]
    """

    kwargs = _get_kwargs(
        path=path,
        download=download,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    download: Union[Unset, bool] = UNSET,
) -> Union[ErrorResponse, Union["Directory", "FileWithContent", File]] | None:
    """Get file or directory information

     Get content of a file or listing of a directory. Use Accept header to control response format for
    files.

    Args:
        path (str):
        download (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, Union['Directory', 'FileWithContent', File]]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            download=download,
        )
    ).parsed
