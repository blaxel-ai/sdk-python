Module blaxel.core.client.api.public_ipslist.list_public_ips
============================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.public_ips.PublicIps | None`
:   List public ips
    
     Returns a list of all public ips used in Blaxel..
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PublicIps

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.public_ips.PublicIps]`
:   List public ips
    
     Returns a list of all public ips used in Blaxel..
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PublicIps]

`sync(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.public_ips.PublicIps | None`
:   List public ips
    
     Returns a list of all public ips used in Blaxel..
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PublicIps

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.public_ips.PublicIps]`
:   List public ips
    
     Returns a list of all public ips used in Blaxel..
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PublicIps]