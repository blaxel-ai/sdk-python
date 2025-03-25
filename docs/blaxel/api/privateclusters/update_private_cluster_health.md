Module blaxel.api.privateclusters.update_private_cluster_health
===============================================================

Functions
---------

`asyncio_detailed(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[typing.Any]`
:   Update private cluster health
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[typing.Any]`
:   Update private cluster health
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]