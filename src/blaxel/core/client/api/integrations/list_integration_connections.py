from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.integration_connection import IntegrationConnection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    external_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["externalId"] = external_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/integrations/connections",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Error, list["IntegrationConnection"]] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = IntegrationConnection.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Error, list["IntegrationConnection"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    external_id: Union[Unset, str] = UNSET,
) -> Response[Union[Error, list["IntegrationConnection"]]]:
    """List integration connections

     Returns all configured integration connections in the workspace. Each connection stores credentials
    and settings for an external service (LLM provider, API, database).

    Args:
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['IntegrationConnection']]]
    """

    kwargs = _get_kwargs(
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    external_id: Union[Unset, str] = UNSET,
) -> Union[Error, list["IntegrationConnection"]] | None:
    """List integration connections

     Returns all configured integration connections in the workspace. Each connection stores credentials
    and settings for an external service (LLM provider, API, database).

    Args:
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['IntegrationConnection']]
    """

    return sync_detailed(
        client=client,
        external_id=external_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    external_id: Union[Unset, str] = UNSET,
) -> Response[Union[Error, list["IntegrationConnection"]]]:
    """List integration connections

     Returns all configured integration connections in the workspace. Each connection stores credentials
    and settings for an external service (LLM provider, API, database).

    Args:
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, list['IntegrationConnection']]]
    """

    kwargs = _get_kwargs(
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    external_id: Union[Unset, str] = UNSET,
) -> Union[Error, list["IntegrationConnection"]] | None:
    """List integration connections

     Returns all configured integration connections in the workspace. Each connection stores credentials
    and settings for an external service (LLM provider, API, database).

    Args:
        external_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, list['IntegrationConnection']]
    """

    return (
        await asyncio_detailed(
            client=client,
            external_id=external_id,
        )
    ).parsed
