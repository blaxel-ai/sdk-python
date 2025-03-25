Module blaxel.api.integrations.get_integration
==============================================

Functions
---------

`asyncio_detailed(integration_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(integration_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   List integrations connections
    
     Returns integration information by name.
    
    Args:
        integration_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]