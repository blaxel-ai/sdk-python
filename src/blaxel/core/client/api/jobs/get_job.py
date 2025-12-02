from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.model import Model
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    show_secrets: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["show_secrets"] = show_secrets

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{job_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Model | None:
    if response.status_code == 200:
        response_200 = Model.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Model]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: Union[Client],
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Model]:
    """Get job

     Returns a job by name.

    Args:
        job_id (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Model]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        show_secrets=show_secrets,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Union[Client],
    show_secrets: Union[Unset, bool] = UNSET,
) -> Model | None:
    """Get job

     Returns a job by name.

    Args:
        job_id (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Model
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        show_secrets=show_secrets,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Union[Client],
    show_secrets: Union[Unset, bool] = UNSET,
) -> Response[Model]:
    """Get job

     Returns a job by name.

    Args:
        job_id (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Model]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        show_secrets=show_secrets,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Union[Client],
    show_secrets: Union[Unset, bool] = UNSET,
) -> Model | None:
    """Get job

     Returns a job by name.

    Args:
        job_id (str):
        show_secrets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Model
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            show_secrets=show_secrets,
        )
    ).parsed
