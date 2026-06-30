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
    *,
    body: Application,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/applications/{application_name}",
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
) -> Union[Application, Error] | None:
    if response.status_code == 200:
        response_200 = Application.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400
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
    body: Application,
) -> Response[Union[Application, Error]]:
    """Update application

     Updates an application's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        application_name (str):
        body (Application): Long-running application deployment that runs your custom code as a
            publicly accessible endpoint. Applications are always public and use mk3 generation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Application, Error]]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_name: str,
    *,
    client: Client,
    body: Application,
) -> Union[Application, Error] | None:
    """Update application

     Updates an application's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        application_name (str):
        body (Application): Long-running application deployment that runs your custom code as a
            publicly accessible endpoint. Applications are always public and use mk3 generation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Application, Error]
    """

    return sync_detailed(
        application_name=application_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    application_name: str,
    *,
    client: Client,
    body: Application,
) -> Response[Union[Application, Error]]:
    """Update application

     Updates an application's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        application_name (str):
        body (Application): Long-running application deployment that runs your custom code as a
            publicly accessible endpoint. Applications are always public and use mk3 generation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Application, Error]]
    """

    kwargs = _get_kwargs(
        application_name=application_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_name: str,
    *,
    client: Client,
    body: Application,
) -> Union[Application, Error] | None:
    """Update application

     Updates an application's configuration and triggers a new deployment. Changes to runtime settings,
    environment variables, or scaling parameters will be applied on the next deployment.

    Args:
        application_name (str):
        body (Application): Long-running application deployment that runs your custom code as a
            publicly accessible endpoint. Applications are always public and use mk3 generation.

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
            body=body,
        )
    ).parsed
