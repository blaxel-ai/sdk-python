from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.policy import Policy
from ...types import Response


def _get_kwargs(
    policy_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/policies/{policy_name}",
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Policy]:
    if response.status_code == 200:
        response_200 = Policy.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Policy]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    policy_name: str,
    *,
    client: Union[Client],
) -> Response[Policy]:
    """Delete policy

     Deletes a policy by name.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Policy]
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
    client: Union[Client],
) -> Optional[Policy]:
    """Delete policy

     Deletes a policy by name.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Policy
    """

    return sync_detailed(
        policy_name=policy_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    policy_name: str,
    *,
    client: Union[Client],
) -> Response[Policy]:
    """Delete policy

     Deletes a policy by name.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Policy]
    """

    kwargs = _get_kwargs(
        policy_name=policy_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    policy_name: str,
    *,
    client: Union[Client],
) -> Optional[Policy]:
    """Delete policy

     Deletes a policy by name.

    Args:
        policy_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Policy
    """

    return (
        await asyncio_detailed(
            policy_name=policy_name,
            client=client,
        )
    ).parsed
