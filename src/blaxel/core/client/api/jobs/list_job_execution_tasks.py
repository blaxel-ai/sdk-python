from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.job_execution_task_list import JobExecutionTaskList
from ...models.list_job_execution_tasks_sort import ListJobExecutionTasksSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    execution_id: str,
    *,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListJobExecutionTasksSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/{job_id}/executions/{execution_id}/tasks".format(
            job_id=quote(str(job_id), safe=""),
            execution_id=quote(str(execution_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Any | JobExecutionTaskList | None:
    if response.status_code == 200:
        response_200 = JobExecutionTaskList.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Any | JobExecutionTaskList]:
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
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListJobExecutionTasksSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[Any | JobExecutionTaskList]:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListJobExecutionTasksSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecutionTaskList]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        execution_id=execution_id,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
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
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListJobExecutionTasksSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Any | JobExecutionTaskList | None:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListJobExecutionTasksSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecutionTaskList
    """

    return sync_detailed(
        job_id=job_id,
        execution_id=execution_id,
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListJobExecutionTasksSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[Any | JobExecutionTaskList]:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListJobExecutionTasksSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecutionTaskList]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        execution_id=execution_id,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    execution_id: str,
    *,
    client: Client,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 50,
    sort: ListJobExecutionTasksSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Any | JobExecutionTaskList | None:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 50.
        sort (ListJobExecutionTasksSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecutionTaskList
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            execution_id=execution_id,
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
        )
    ).parsed
