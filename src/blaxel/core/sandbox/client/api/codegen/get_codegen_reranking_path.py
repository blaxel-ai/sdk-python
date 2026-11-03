from http import HTTPStatus
from typing import Any
from urllib.parse import quote

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
    score_threshold: float | Unset = UNSET,
    token_limit: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    params["scoreThreshold"] = score_threshold

    params["tokenLimit"] = token_limit

    params["filePattern"] = file_pattern

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/codegen/reranking/{path}".format(
            path=quote(str(path), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Client, response: httpx.Response
) -> ErrorResponse | RerankingResponse | None:
    if response.status_code == 200:
        response_200 = RerankingResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_400, response)
        return response_400

    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_422, response)
        return response_422

    if response.status_code == 503:
        response_503 = ErrorResponse.from_dict(response.json())

        errors.retain_response(response_503, response)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[ErrorResponse | RerankingResponse]:
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
    score_threshold: float | Unset = UNSET,
    token_limit: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
) -> Response[ErrorResponse | RerankingResponse]:
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
        score_threshold (float | Unset):
        token_limit (int | Unset):
        file_pattern (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RerankingResponse]
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
    score_threshold: float | Unset = UNSET,
    token_limit: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
) -> ErrorResponse | RerankingResponse | None:
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
        score_threshold (float | Unset):
        token_limit (int | Unset):
        file_pattern (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RerankingResponse
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
    score_threshold: float | Unset = UNSET,
    token_limit: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
) -> Response[ErrorResponse | RerankingResponse]:
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
        score_threshold (float | Unset):
        token_limit (int | Unset):
        file_pattern (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | RerankingResponse]
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
    score_threshold: float | Unset = UNSET,
    token_limit: int | Unset = UNSET,
    file_pattern: str | Unset = UNSET,
) -> ErrorResponse | RerankingResponse | None:
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
        score_threshold (float | Unset):
        token_limit (int | Unset):
        file_pattern (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | RerankingResponse
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
