Module blaxel.api.integrations.get_integration_connection_model
===============================================================

Functions
---------

`asyncio_detailed(connection_name: str, model_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Get integration model endpoint configurations
    
     Returns a model for an integration connection by ID.
    
    Args:
        connection_name (str):
        model_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(connection_name: str, model_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Get integration model endpoint configurations
    
     Returns a model for an integration connection by ID.
    
    Args:
        connection_name (str):
        model_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]