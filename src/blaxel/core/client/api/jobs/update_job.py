from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.job import Job
from ...types import Response


def _get_kwargs(
    job_id: str,
    *,
    body: Job,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/jobs/{job_id}",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Job | None:
    if response.status_code == 200:
        response_200 = Job.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Job]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: Client,
    body: Job,
) -> Response[Job]:
    """Update batch job

     Updates a batch job's configuration. Changes affect new executions; running executions continue with
    their original configuration.

    Args:
        job_id (str):
        body (Job): Batch processing job definition for running parallel AI tasks. Jobs can
            execute multiple tasks concurrently with configurable parallelism, retries, and timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Job]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Client,
    body: Job,
) -> Job | None:
    """Update batch job

     Updates a batch job's configuration. Changes affect new executions; running executions continue with
    their original configuration.

    Args:
        job_id (str):
        body (Job): Batch processing job definition for running parallel AI tasks. Jobs can
            execute multiple tasks concurrently with configurable parallelism, retries, and timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Job
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Client,
    body: Job,
) -> Response[Job]:
    """Update batch job

     Updates a batch job's configuration. Changes affect new executions; running executions continue with
    their original configuration.

    Args:
        job_id (str):
        body (Job): Batch processing job definition for running parallel AI tasks. Jobs can
            execute multiple tasks concurrently with configurable parallelism, retries, and timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Job]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Client,
    body: Job,
) -> Job | None:
    """Update batch job

     Updates a batch job's configuration. Changes affect new executions; running executions continue with
    their original configuration.

    Args:
        job_id (str):
        body (Job): Batch processing job definition for running parallel AI tasks. Jobs can
            execute multiple tasks concurrently with configurable parallelism, retries, and timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Job
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            body=body,
        )
    ).parsed
