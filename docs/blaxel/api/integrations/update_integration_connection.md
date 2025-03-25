Module blaxel.api.integrations.update_integration_connection
============================================================

Functions
---------

`asyncio(connection_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client, body: blaxel.models.integration_connection.IntegrationConnection) ‑> blaxel.models.integration_connection.IntegrationConnection | None`
:   Update integration connection
    
     Update an integration connection by integration name and connection name.
    
    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        IntegrationConnection

`asyncio_detailed(connection_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client, body: blaxel.models.integration_connection.IntegrationConnection) ‑> blaxel.types.Response[blaxel.models.integration_connection.IntegrationConnection]`
:   Update integration connection
    
     Update an integration connection by integration name and connection name.
    
    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[IntegrationConnection]

`sync(connection_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client, body: blaxel.models.integration_connection.IntegrationConnection) ‑> blaxel.models.integration_connection.IntegrationConnection | None`
:   Update integration connection
    
     Update an integration connection by integration name and connection name.
    
    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        IntegrationConnection

`sync_detailed(connection_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client, body: blaxel.models.integration_connection.IntegrationConnection) ‑> blaxel.types.Response[blaxel.models.integration_connection.IntegrationConnection]`
:   Update integration connection
    
     Update an integration connection by integration name and connection name.
    
    Args:
        connection_name (str):
        body (IntegrationConnection): Integration Connection
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[IntegrationConnection]