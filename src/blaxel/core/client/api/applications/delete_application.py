from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.application import Application
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    application_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/applications/{application_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Application, Error] | None:
    if response.status_code == 200:
        response_200 = Application.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Application, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_name: str,
    *,
    client: Client,
) -> Response[Union[Application, Error]]:
    """Delete application

     Permanently deletes an application and all its deployment history. The application endpoint will
    immediately stop responding. This action cannot be undone.

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Application, Error]]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_name: str,
    *,
    client: Client,
) -> Union[Application, Error] | None:
    """Delete application

     Permanently deletes an application and all its deployment history. The application endpoint will
    immediately stop responding. This action cannot be undone.

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Application, Error]
    """

    return sync_detailed(
        application_name=application_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    application_name: str,
    *,
    client: Client,
) -> Response[Union[Application, Error]]:
    """Delete application

     Permanently deletes an application and all its deployment history. The application endpoint will
    immediately stop responding. This action cannot be undone.

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Application, Error]]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_name: str,
    *,
    client: Client,
) -> Union[Application, Error] | None:
    """Delete application

     Permanently deletes an application and all its deployment history. The application endpoint will
    immediately stop responding. This action cannot be undone.

    Args:
        application_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Application, Error]
    """

    return (
        await asyncio_detailed(
            application_name=application_name,
            client=client,
        )
    ).parsed
