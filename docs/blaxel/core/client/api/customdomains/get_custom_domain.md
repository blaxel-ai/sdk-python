Module blaxel.core.client.api.customdomains.get_custom_domain
=============================================================

Functions
---------

`asyncio(domain_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.custom_domain.CustomDomain | None`
:   Get custom domain
    
    Args:
        domain_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CustomDomain

`asyncio_detailed(domain_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.custom_domain.CustomDomain]`
:   Get custom domain
    
    Args:
        domain_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CustomDomain]

`sync(domain_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.custom_domain.CustomDomain | None`
:   Get custom domain
    
    Args:
        domain_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CustomDomain

`sync_detailed(domain_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.custom_domain.CustomDomain]`
:   Get custom domain
    
    Args:
        domain_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CustomDomain]