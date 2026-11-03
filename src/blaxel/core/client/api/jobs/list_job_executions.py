from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.job_execution_list import JobExecutionList
from ...models.list_job_executions_sort import ListJobExecutionsSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    sort: ListJobExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["cursor"] = cursor

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/jobs/{job_id}/executions".format(
            job_id=quote(str(job_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | JobExecutionList | None:
    if response.status_code == 200:
        response_200 = JobExecutionList.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        errors.retain_response(response_400, response)
        return response_400

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
) -> Response[Any | JobExecutionList]:
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
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    sort: ListJobExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[Any | JobExecutionList]:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.
        cursor (str | Unset):
        sort (ListJobExecutionsSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecutionList]
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
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    sort: ListJobExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Any | JobExecutionList | None:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.
        cursor (str | Unset):
        sort (ListJobExecutionsSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecutionList
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
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    sort: ListJobExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Response[Any | JobExecutionList]:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.
        cursor (str | Unset):
        sort (ListJobExecutionsSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | JobExecutionList]
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
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    cursor: str | Unset = UNSET,
    sort: ListJobExecutionsSort | Unset = UNSET,
    q: str | Unset = UNSET,
) -> Any | JobExecutionList | None:
    """List job executions

     Returns executions for a batch job. Starting with API version 2026-04-28 the response is wrapped in
    `{data, meta}` and supports cursor pagination via the `cursor` and `limit` query parameters; older
    versions keep the legacy offset/limit contract and return a bare array.

    Args:
        job_id (str):
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.
        cursor (str | Unset):
        sort (ListJobExecutionsSort | Unset):
        q (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | JobExecutionList
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
