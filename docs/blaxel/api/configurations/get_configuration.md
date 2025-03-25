Module blaxel.api.configurations.get_configuration
==================================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.configuration.Configuration | None`
:   List all configurations
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Configuration

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.configuration.Configuration]`
:   List all configurations
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Configuration]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.configuration.Configuration | None`
:   List all configurations
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Configuration

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.configuration.Configuration]`
:   List all configurations
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Configuration]