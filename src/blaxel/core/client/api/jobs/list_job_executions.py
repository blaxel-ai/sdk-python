from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.job_execution_list import JobExecutionList
from ...models.list_job_executions_sort import ListJobExecutionsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListJobExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["cursor"] = cursor

    json_sort: Union[Unset, str] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{job_id}/executions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, JobExecutionList] | None:
    if response.status_code == 200:
        response_200 = JobExecutionList.from_dict(response.json())

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


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, JobExecutionList]]:
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
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListJobExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[Union[Any, JobExecutionList]]:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListJobExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecutionList]]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        limit=limit,
        offset=offset,
        cursor=cursor,
        sort=sort,
        q=q,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListJobExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Union[Any, JobExecutionList] | None:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListJobExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecutionList]
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        limit=limit,
        offset=offset,
        cursor=cursor,
        sort=sort,
        q=q,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListJobExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Response[Union[Any, JobExecutionList]]:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListJobExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, JobExecutionList]]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        limit=limit,
        offset=offset,
        cursor=cursor,
        sort=sort,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
    cursor: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListJobExecutionsSort] = UNSET,
    q: Union[Unset, str] = UNSET,
) -> Union[Any, JobExecutionList] | None:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
        cursor (Union[Unset, str]):
        sort (Union[Unset, ListJobExecutionsSort]):
        q (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, JobExecutionList]
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            limit=limit,
            offset=offset,
            cursor=cursor,
            sort=sort,
            q=q,
        )
    ).parsed
