from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.custom_domain import CustomDomain
from ...models.share_custom_domain_body import ShareCustomDomainBody
from ...types import Response


def _get_kwargs(
    domain_name: str,
    *,
    body: ShareCustomDomainBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/customdomains/{domain_name}/share",
    }

    if type(body) is dict:
        _body = body
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Client, response: httpx.Response) -> Union[Any, CustomDomain] | None:
    if response.status_code == 200:
        response_200 = CustomDomain.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    if client.raise_on_unexpected_status:
        raise errors.from_response(response.status_code, response.content, response.headers)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, CustomDomain]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain_name: str,
    *,
    client: Client,
    body: ShareCustomDomainBody,
) -> Response[Union[Any, CustomDomain]]:
    r"""Share a custom domain

     Shares a verified custom domain with another workspace of the same account by copying the domain
    record; the ACM certificate and CloudFront tenant stay with the owner and are reused (not re-
    provisioned). Use targetWorkspace \"account\" to make the domain usable by every workspace of the
    account. Cross-account sharing is not supported.

    Args:
        domain_name (str):
        body (ShareCustomDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CustomDomain]]
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
    client: Client,
    body: ShareCustomDomainBody,
) -> Union[Any, CustomDomain] | None:
    r"""Share a custom domain

     Shares a verified custom domain with another workspace of the same account by copying the domain
    record; the ACM certificate and CloudFront tenant stay with the owner and are reused (not re-
    provisioned). Use targetWorkspace \"account\" to make the domain usable by every workspace of the
    account. Cross-account sharing is not supported.

    Args:
        domain_name (str):
        body (ShareCustomDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CustomDomain]
    """

    return sync_detailed(
        domain_name=domain_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain_name: str,
    *,
    client: Client,
    body: ShareCustomDomainBody,
) -> Response[Union[Any, CustomDomain]]:
    r"""Share a custom domain

     Shares a verified custom domain with another workspace of the same account by copying the domain
    record; the ACM certificate and CloudFront tenant stay with the owner and are reused (not re-
    provisioned). Use targetWorkspace \"account\" to make the domain usable by every workspace of the
    account. Cross-account sharing is not supported.

    Args:
        domain_name (str):
        body (ShareCustomDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CustomDomain]]
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
    client: Client,
    body: ShareCustomDomainBody,
) -> Union[Any, CustomDomain] | None:
    r"""Share a custom domain

     Shares a verified custom domain with another workspace of the same account by copying the domain
    record; the ACM certificate and CloudFront tenant stay with the owner and are reused (not re-
    provisioned). Use targetWorkspace \"account\" to make the domain usable by every workspace of the
    account. Cross-account sharing is not supported.

    Args:
        domain_name (str):
        body (ShareCustomDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CustomDomain]
    """

    return (
        await asyncio_detailed(
            domain_name=domain_name,
            client=client,
            body=body,
        )
    ).parsed
