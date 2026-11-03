from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.job_execution import JobExecution
from ...types import Response


def _get_kwargs(
    job_id: str,
    execution_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/jobs/{job_id}/executions/{execution_id}".format(
            job_id=quote(str(job_id), safe=""),
            execution_id=quote(str(execution_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | JobExecution | None:
    if response.status_code == 200:
        response_200 = JobExecution.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 404:
        response_404 = cast(Any, None)
        errors.retain_response(response_404, response)
        return response_404

    if response.status_code == 500:
        response_500 = cast(Any, None)
        errors.retain_response(response_500, response)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | JobExecution]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
) -> Response[Any | JobExecution]:
    """Cancel job execution

     Cancels a running job execution. Tasks already in progress will complete, but no new tasks will be
    started. The execution status changes to 'cancelling' then 'cancelled'.

    Args:
        job_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecution]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        execution_id=execution_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
) -> Any | JobExecution | None:
    """Cancel job execution

     Cancels a running job execution. Tasks already in progress will complete, but no new tasks will be
    started. The execution status changes to 'cancelling' then 'cancelled'.

    Args:
        job_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecution
    """

    return sync_detailed(
        job_id=job_id,
        execution_id=execution_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
) -> Response[Any | JobExecution]:
    """Cancel job execution

     Cancels a running job execution. Tasks already in progress will complete, but no new tasks will be
    started. The execution status changes to 'cancelling' then 'cancelled'.

    Args:
        job_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecution]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        execution_id=execution_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
) -> Any | JobExecution | None:
    """Cancel job execution

     Cancels a running job execution. Tasks already in progress will complete, but no new tasks will be
    started. The execution status changes to 'cancelling' then 'cancelled'.

    Args:
        job_id (str):
        execution_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecution
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            execution_id=execution_id,
            client=client,
        )
    ).parsed
