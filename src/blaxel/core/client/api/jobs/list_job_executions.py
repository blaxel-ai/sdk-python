from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.job_execution import JobExecution
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/jobs/{job_id}/executions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[Any, list["JobExecution"]] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = JobExecution.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, list["JobExecution"]]]:
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
) -> Response[Union[Any, list["JobExecution"]]]:
    """List job executions

     Returns paginated list of executions for a batch job, sorted by creation time. Each execution
    contains status, task counts, and timing information.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['JobExecution']]]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        limit=limit,
        offset=offset,
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
) -> Union[Any, list["JobExecution"]] | None:
    """List job executions

     Returns paginated list of executions for a batch job, sorted by creation time. Each execution
    contains status, task counts, and timing information.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['JobExecution']]
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
) -> Response[Union[Any, list["JobExecution"]]]:
    """List job executions

     Returns paginated list of executions for a batch job, sorted by creation time. Each execution
    contains status, task counts, and timing information.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, list['JobExecution']]]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Client,
    limit: Union[Unset, int] = 20,
    offset: Union[Unset, int] = 0,
) -> Union[Any, list["JobExecution"]] | None:
    """List job executions

     Returns paginated list of executions for a batch job, sorted by creation time. Each execution
    contains status, task counts, and timing information.

    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, list['JobExecution']]
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
