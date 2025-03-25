Module blaxel.api.integrations.list_integration_connection_models
=================================================================

Functions
---------

`asyncio_detailed(connection_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   List integration connection models
    
     Returns a list of all models for an integration connection.
    
    Args:
        connection_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(connection_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   List integration connection models
    
     Returns a list of all models for an integration connection.
    
    Args:
        connection_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]