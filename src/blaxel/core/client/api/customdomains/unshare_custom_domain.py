from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import Client
from ...models.custom_domain import CustomDomain
from ...types import Response


def _get_kwargs(
    domain_name: str,
    target_workspace: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/customdomains/{domain_name}/share/{target_workspace}".format(
            domain_name=quote(str(domain_name), safe=""),
            target_workspace=quote(str(target_workspace), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Any | CustomDomain | None:
    if response.status_code == 200:
        response_200 = CustomDomain.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        errors.retain_response(response_404, response)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.from_response(
            response.status_code, response.content, response.headers, response=response
        )
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any | CustomDomain]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Response[Any | CustomDomain]:
    """Unshare a custom domain

     Revokes sharing of a custom domain with a target workspace (or the account when targetWorkspace is
    "account"). Removes the shared copy / clears the account-global marker; the owner's domain is not
    affected.

    Args:
        domain_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CustomDomain]
    """

    kwargs = _get_kwargs(
        domain_name=domain_name,
        target_workspace=target_workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Any | CustomDomain | None:
    """Unshare a custom domain

     Revokes sharing of a custom domain with a target workspace (or the account when targetWorkspace is
    "account"). Removes the shared copy / clears the account-global marker; the owner's domain is not
    affected.

    Args:
        domain_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CustomDomain
    """

    return sync_detailed(
        domain_name=domain_name,
        target_workspace=target_workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    domain_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Response[Any | CustomDomain]:
    """Unshare a custom domain

     Revokes sharing of a custom domain with a target workspace (or the account when targetWorkspace is
    "account"). Removes the shared copy / clears the account-global marker; the owner's domain is not
    affected.

    Args:
        domain_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CustomDomain]
    """

    kwargs = _get_kwargs(
        domain_name=domain_name,
        target_workspace=target_workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_name: str,
    target_workspace: str,
    *,
    client: Client,
) -> Any | CustomDomain | None:
    """Unshare a custom domain

     Revokes sharing of a custom domain with a target workspace (or the account when targetWorkspace is
    "account"). Removes the shared copy / clears the account-global marker; the owner's domain is not
    affected.

    Args:
        domain_name (str):
        target_workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CustomDomain
    """

    return (
        await asyncio_detailed(
            domain_name=domain_name,
            target_workspace=target_workspace,
            client=client,
        )
    ).parsed
