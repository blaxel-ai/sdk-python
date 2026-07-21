from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import Client
from ...models.policy_usages import PolicyUsages
from ...types import Response


def _get_kwargs(
    policy_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/policies/{policy_name}/usages",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> PolicyUsages | None:
    if response.status_code == 200:
        response_200 = PolicyUsages.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[PolicyUsages]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    policy_name: str,
    *,
    client: Client,
) -> Response[PolicyUsages]:
    """List resources using a policy

     Returns the names of every resource (agent, function, model, sandbox, job) currently referencing the
    given policy. Replaces the client-side fan-out the policies UI used to do over the listings.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PolicyUsages]
    """

    kwargs = _get_kwargs(
        policy_name=policy_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    policy_name: str,
    *,
    client: Client,
) -> PolicyUsages | None:
    """List resources using a policy

     Returns the names of every resource (agent, function, model, sandbox, job) currently referencing the
    given policy. Replaces the client-side fan-out the policies UI used to do over the listings.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PolicyUsages
    """

    return sync_detailed(
        policy_name=policy_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    policy_name: str,
    *,
    client: Client,
) -> Response[PolicyUsages]:
    """List resources using a policy

     Returns the names of every resource (agent, function, model, sandbox, job) currently referencing the
    given policy. Replaces the client-side fan-out the policies UI used to do over the listings.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PolicyUsages]
    """

    kwargs = _get_kwargs(
        policy_name=policy_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    policy_name: str,
    *,
    client: Client,
) -> PolicyUsages | None:
    """List resources using a policy

     Returns the names of every resource (agent, function, model, sandbox, job) currently referencing the
    given policy. Replaces the client-side fan-out the policies UI used to do over the listings.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PolicyUsages
    """

    return (
        await asyncio_detailed(
            policy_name=policy_name,
            client=client,
        )
    ).parsed
