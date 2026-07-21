from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.job_list import JobList
from ...models.list_jobs_anchor import ListJobsAnchor
from ...models.list_jobs_sort import ListJobsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListJobsAnchor] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cursor"] = cursor

    params["limit"] = limit

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    json_anchor: Union[Unset, str] = UNSET
    if not isinstance(anchor, Unset):
        json_anchor = anchor.value

    params["anchor"] = json_anchor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> JobList | None:
    if response.status_code == 200:
        response_200 = JobList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[JobList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListJobsAnchor] = UNSET,
) -> Response[JobList]:
    """List batch jobs

     Returns batch job definitions in the workspace. Each job can be triggered to run multiple parallel
    tasks with configurable concurrency and retry settings. Starting with API version 2026-04-28 the
    response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit`
    query parameters; older versions keep returning a bare array with all jobs.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListJobsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListJobsAnchor] = UNSET,
) -> JobList | None:
    """List batch jobs

     Returns batch job definitions in the workspace. Each job can be triggered to run multiple parallel
    tasks with configurable concurrency and retry settings. Starting with API version 2026-04-28 the
    response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit`
    query parameters; older versions keep returning a bare array with all jobs.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListJobsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobList
    """

    return sync_detailed(
        client=client,
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListJobsAnchor] = UNSET,
) -> Response[JobList]:
    """List batch jobs

     Returns batch job definitions in the workspace. Each job can be triggered to run multiple parallel
    tasks with configurable concurrency and retry settings. Starting with API version 2026-04-28 the
    response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit`
    query parameters; older versions keep returning a bare array with all jobs.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListJobsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[JobList]
    """

    kwargs = _get_kwargs(
        cursor=cursor,
        limit=limit,
        sort=sort,
        q=q,
        anchor=anchor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    sort: Union[Unset, ListJobsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
    anchor: Union[Unset, ListJobsAnchor] = UNSET,
) -> JobList | None:
    """List batch jobs

     Returns batch job definitions in the workspace. Each job can be triggered to run multiple parallel
    tasks with configurable concurrency and retry settings. Starting with API version 2026-04-28 the
    response is wrapped in `{data, meta}` and supports cursor pagination via the `cursor` and `limit`
    query parameters; older versions keep returning a bare array with all jobs.

    Args:
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        sort (Union[Unset, ListJobsSort]):
        q (Union[Unset, str]):
        anchor (Union[Unset, ListJobsAnchor]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        JobList
    """

    return (
        await asyncio_detailed(
            client=client,
            cursor=cursor,
            limit=limit,
            sort=sort,
            q=q,
            anchor=anchor,
        )
    ).parsed
