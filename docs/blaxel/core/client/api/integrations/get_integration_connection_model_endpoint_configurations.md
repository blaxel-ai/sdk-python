Module blaxel.core.client.api.integrations.get_integration_connection_model_endpoint_configurations
===================================================================================================

Functions
---------

`asyncio_detailed(connection_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[typing.Any]`
:   Get integration connection model endpoint configurations
    
     Returns a list of all endpoint configurations for a model.
    
    Args:
        connection_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(connection_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[typing.Any]`
:   Get integration connection model endpoint configurations
    
     Returns a list of all endpoint configurations for a model.
    
    Args:
        connection_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]