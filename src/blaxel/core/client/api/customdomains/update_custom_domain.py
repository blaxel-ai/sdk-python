from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.custom_domain import CustomDomain
from ...types import Response


def _get_kwargs(
    domain_name: str,
    *,
    body: CustomDomain,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/customdomains/{domain_name}",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[CustomDomain]:
    if response.status_code == 200:
        response_200 = CustomDomain.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[CustomDomain]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_name: str,
    *,
    client: Union[Client],
    body: CustomDomain,
) -> Response[CustomDomain]:
    """Update custom domain

    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomDomain]
    """

    kwargs = _get_kwargs(
        domain_name=domain_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain_name: str,
    *,
    client: Union[Client],
    body: CustomDomain,
) -> Optional[CustomDomain]:
    """Update custom domain

    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomDomain
    """

    return sync_detailed(
        domain_name=domain_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_name: str,
    *,
    client: Union[Client],
    body: CustomDomain,
) -> Response[CustomDomain]:
    """Update custom domain

    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomDomain]
    """

    kwargs = _get_kwargs(
        domain_name=domain_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain_name: str,
    *,
    client: Union[Client],
    body: CustomDomain,
) -> Optional[CustomDomain]:
    """Update custom domain

    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomDomain
    """

    return (
        await asyncio_detailed(
            domain_name=domain_name,
            client=client,
            body=body,
        )
    ).parsed
