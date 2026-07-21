from http import HTTPStatus
from typing import Any, Union, cast

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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobExecutionTasksSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{job_id}/executions/{execution_id}/tasks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, JobExecutionTaskList] | None:
    if response.status_code == 200:
        response_200 = JobExecutionTaskList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, JobExecutionTaskList]]:
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobExecutionTasksSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[Union[Any, JobExecutionTaskList]]:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobExecutionTasksSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecutionTaskList]]
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobExecutionTasksSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Union[Any, JobExecutionTaskList] | None:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobExecutionTasksSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecutionTaskList]
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobExecutionTasksSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[Union[Any, JobExecutionTaskList]]:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobExecutionTasksSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecutionTaskList]]
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
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobExecutionTasksSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Union[Any, JobExecutionTaskList] | None:
    """List execution tasks

     Returns one cursor-paginated page of an execution's tasks. Tasks are derived from event history each
    request; only the in-memory slicing is paginated, the events scan still fetches the whole event log
    behind the scenes. Available starting with API version 2026-04-28.

    Args:
        job_id (str):
        execution_id (str):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobExecutionTasksSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecutionTaskList]
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
