from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.model import Model
from ...types import Response


def _get_kwargs(
    model_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/models/{model_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Error, Model] | None:
    if response.status_code == 200:
        response_200 = Model.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Error, Model]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    model_name: str,
    *,
    client: Client,
) -> Response[Union[Error, Model]]:
    """Delete model endpoint

     Permanently deletes a model gateway endpoint. Any agents or applications using this endpoint will
    need to be updated to use a different model.

    Args:
        model_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Model]]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    model_name: str,
    *,
    client: Client,
) -> Union[Error, Model] | None:
    """Delete model endpoint

     Permanently deletes a model gateway endpoint. Any agents or applications using this endpoint will
    need to be updated to use a different model.

    Args:
        model_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Model]
    """

    return sync_detailed(
        model_name=model_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    model_name: str,
    *,
    client: Client,
) -> Response[Union[Error, Model]]:
    """Delete model endpoint

     Permanently deletes a model gateway endpoint. Any agents or applications using this endpoint will
    need to be updated to use a different model.

    Args:
        model_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, Model]]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_name: str,
    *,
    client: Client,
) -> Union[Error, Model] | None:
    """Delete model endpoint

     Permanently deletes a model gateway endpoint. Any agents or applications using this endpoint will
    need to be updated to use a different model.

    Args:
        model_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, Model]
    """

    return (
        await asyncio_detailed(
            model_name=model_name,
            client=client,
        )
    ).parsed
