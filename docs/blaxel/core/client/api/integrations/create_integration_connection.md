Module blaxel.core.client.api.integrations.create_integration_connection
========================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.integration_connection.IntegrationConnection) ‑> blaxel.core.client.models.integration_connection.IntegrationConnection | None`
:   Create integration
    
     Create a connection for an integration.
    
    Args:
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        IntegrationConnection

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.integration_connection.IntegrationConnection) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.integration_connection.IntegrationConnection]`
:   Create integration
    
     Create a connection for an integration.
    
    Args:
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[IntegrationConnection]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.integration_connection.IntegrationConnection) ‑> blaxel.core.client.models.integration_connection.IntegrationConnection | None`
:   Create integration
    
     Create a connection for an integration.
    
    Args:
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        IntegrationConnection

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.integration_connection.IntegrationConnection) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.integration_connection.IntegrationConnection]`
:   Create integration
    
     Create a connection for an integration.
    
    Args:
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[IntegrationConnection]