from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.error import Error
from ...models.model import Model
from ...types import Response


def _get_kwargs(
    model_name: str,
    *,
    body: Model,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/models/{model_name}".format(
            model_name=quote(str(model_name), safe=""),
        ),
    }

    if type(body) is dict:
        _kwargs["json"] = body
    else:
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Error | Model | None:
    if response.status_code == 200:
        response_200 = Model.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        errors.retain_response(response_401, response)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        errors.retain_response(response_403, response)
        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Error | Model]:
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
    body: Model,
) -> Response[Error | Model]:
    """Update model endpoint

     Updates a model gateway endpoint's configuration. Changes to provider settings or integration
    connection take effect immediately.

    Args:
        model_name (str):
        body (Model): Gateway endpoint to external LLM provider APIs (OpenAI, Anthropic, etc.)
            with unified access control, credentials management, and usage tracking.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Model]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    model_name: str,
    *,
    client: Client,
    body: Model,
) -> Error | Model | None:
    """Update model endpoint

     Updates a model gateway endpoint's configuration. Changes to provider settings or integration
    connection take effect immediately.

    Args:
        model_name (str):
        body (Model): Gateway endpoint to external LLM provider APIs (OpenAI, Anthropic, etc.)
            with unified access control, credentials management, and usage tracking.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Model
    """

    return sync_detailed(
        model_name=model_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    model_name: str,
    *,
    client: Client,
    body: Model,
) -> Response[Error | Model]:
    """Update model endpoint

     Updates a model gateway endpoint's configuration. Changes to provider settings or integration
    connection take effect immediately.

    Args:
        model_name (str):
        body (Model): Gateway endpoint to external LLM provider APIs (OpenAI, Anthropic, etc.)
            with unified access control, credentials management, and usage tracking.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Model]
    """

    kwargs = _get_kwargs(
        model_name=model_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_name: str,
    *,
    client: Client,
    body: Model,
) -> Error | Model | None:
    """Update model endpoint

     Updates a model gateway endpoint's configuration. Changes to provider settings or integration
    connection take effect immediately.

    Args:
        model_name (str):
        body (Model): Gateway endpoint to external LLM provider APIs (OpenAI, Anthropic, etc.)
            with unified access control, credentials management, and usage tracking.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Model
    """

    return (
        await asyncio_detailed(
            model_name=model_name,
            client=client,
            body=body,
        )
    ).parsed
