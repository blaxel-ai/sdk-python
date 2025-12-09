from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.reranking_response import RerankingResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    path: str,
    *,
    query: str,
    score_threshold: Union[Unset, float] = UNSET,
    token_limit: Union[Unset, int] = UNSET,
    file_pattern: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    params["scoreThreshold"] = score_threshold

    params["tokenLimit"] = token_limit

    params["filePattern"] = file_pattern

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/codegen/reranking/{path}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Union[ErrorResponse, RerankingResponse] | None:
    if response.status_code == 200:
        response_200 = RerankingResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, RerankingResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    path: str,
    *,
    client: Client,
    query: str,
    score_threshold: Union[Unset, float] = UNSET,
    token_limit: Union[Unset, int] = UNSET,
    file_pattern: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, RerankingResponse]]:
    """Code reranking/semantic search

     Uses Relace's code reranking model to find the most relevant files for a given query. This is useful
    as a first pass in agentic exploration to narrow down the search space.

    Based on: https://docs.relace.ai/docs/code-reranker/agent

    Query Construction: The query can be a short question or a more detailed conversation with the user
    request included. For a first pass, use the full conversation; for subsequent calls, use more
    targeted questions.

    Token Limit and Score Threshold: For 200k token context models like Claude 4 Sonnet, recommended
    defaults are scoreThreshold=0.5 and tokenLimit=30000.

    The response will be a list of file paths and contents ordered from most relevant to least relevant.

    Args:
        path (str):
        query (str):
        score_threshold (Union[Unset, float]):
        token_limit (Union[Unset, int]):
        file_pattern (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RerankingResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        query=query,
        score_threshold=score_threshold,
        token_limit=token_limit,
        file_pattern=file_pattern,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    path: str,
    *,
    client: Client,
    query: str,
    score_threshold: Union[Unset, float] = UNSET,
    token_limit: Union[Unset, int] = UNSET,
    file_pattern: Union[Unset, str] = UNSET,
) -> Union[ErrorResponse, RerankingResponse] | None:
    """Code reranking/semantic search

     Uses Relace's code reranking model to find the most relevant files for a given query. This is useful
    as a first pass in agentic exploration to narrow down the search space.

    Based on: https://docs.relace.ai/docs/code-reranker/agent

    Query Construction: The query can be a short question or a more detailed conversation with the user
    request included. For a first pass, use the full conversation; for subsequent calls, use more
    targeted questions.

    Token Limit and Score Threshold: For 200k token context models like Claude 4 Sonnet, recommended
    defaults are scoreThreshold=0.5 and tokenLimit=30000.

    The response will be a list of file paths and contents ordered from most relevant to least relevant.

    Args:
        path (str):
        query (str):
        score_threshold (Union[Unset, float]):
        token_limit (Union[Unset, int]):
        file_pattern (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RerankingResponse]
    """

    return sync_detailed(
        path=path,
        client=client,
        query=query,
        score_threshold=score_threshold,
        token_limit=token_limit,
        file_pattern=file_pattern,
    ).parsed


async def asyncio_detailed(
    path: str,
    *,
    client: Client,
    query: str,
    score_threshold: Union[Unset, float] = UNSET,
    token_limit: Union[Unset, int] = UNSET,
    file_pattern: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, RerankingResponse]]:
    """Code reranking/semantic search

     Uses Relace's code reranking model to find the most relevant files for a given query. This is useful
    as a first pass in agentic exploration to narrow down the search space.

    Based on: https://docs.relace.ai/docs/code-reranker/agent

    Query Construction: The query can be a short question or a more detailed conversation with the user
    request included. For a first pass, use the full conversation; for subsequent calls, use more
    targeted questions.

    Token Limit and Score Threshold: For 200k token context models like Claude 4 Sonnet, recommended
    defaults are scoreThreshold=0.5 and tokenLimit=30000.

    The response will be a list of file paths and contents ordered from most relevant to least relevant.

    Args:
        path (str):
        query (str):
        score_threshold (Union[Unset, float]):
        token_limit (Union[Unset, int]):
        file_pattern (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RerankingResponse]]
    """

    kwargs = _get_kwargs(
        path=path,
        query=query,
        score_threshold=score_threshold,
        token_limit=token_limit,
        file_pattern=file_pattern,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    path: str,
    *,
    client: Client,
    query: str,
    score_threshold: Union[Unset, float] = UNSET,
    token_limit: Union[Unset, int] = UNSET,
    file_pattern: Union[Unset, str] = UNSET,
) -> Union[ErrorResponse, RerankingResponse] | None:
    """Code reranking/semantic search

     Uses Relace's code reranking model to find the most relevant files for a given query. This is useful
    as a first pass in agentic exploration to narrow down the search space.

    Based on: https://docs.relace.ai/docs/code-reranker/agent

    Query Construction: The query can be a short question or a more detailed conversation with the user
    request included. For a first pass, use the full conversation; for subsequent calls, use more
    targeted questions.

    Token Limit and Score Threshold: For 200k token context models like Claude 4 Sonnet, recommended
    defaults are scoreThreshold=0.5 and tokenLimit=30000.

    The response will be a list of file paths and contents ordered from most relevant to least relevant.

    Args:
        path (str):
        query (str):
        score_threshold (Union[Unset, float]):
        token_limit (Union[Unset, int]):
        file_pattern (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RerankingResponse]
    """

    return (
        await asyncio_detailed(
            path=path,
            client=client,
            query=query,
            score_threshold=score_threshold,
            token_limit=token_limit,
            file_pattern=file_pattern,
        )
    ).parsed
