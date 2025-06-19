Module blaxel.core.client.api.integrations.get_integration
==========================================================

Functions
---------

`asyncio(integration_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.integration.Integration | None`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Integration

`asyncio_detailed(integration_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.integration.Integration]`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Integration]

`sync(integration_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.integration.Integration | None`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Integration

`sync_detailed(integration_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.integration.Integration]`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Integration]