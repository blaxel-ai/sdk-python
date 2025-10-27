from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.create_job_execution_request import CreateJobExecutionRequest
from ...models.job_execution import JobExecution
from ...types import Response


def _get_kwargs(
    job_id: str,
    *,
    body: CreateJobExecutionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/jobs/{job_id}/executions",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, JobExecution] | None:
    if response.status_code == 200:
        response_200 = JobExecution.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, JobExecution]]:
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
    body: CreateJobExecutionRequest,
) -> Response[Union[Any, JobExecution]]:
    """Create job execution

     Creates a new execution for a job by name.

    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecution]]
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
    client: Union[Client],
    body: CreateJobExecutionRequest,
) -> Union[Any, JobExecution] | None:
    """Create job execution

     Creates a new execution for a job by name.

    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecution]
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Union[Client],
    body: CreateJobExecutionRequest,
) -> Response[Union[Any, JobExecution]]:
    """Create job execution

     Creates a new execution for a job by name.

    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecution]]
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
    client: Union[Client],
    body: CreateJobExecutionRequest,
) -> Union[Any, JobExecution] | None:
    """Create job execution

     Creates a new execution for a job by name.

    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecution]
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            body=body,
        )
    ).parsed
