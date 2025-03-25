Module blaxel.api.privateclusters.delete_private_cluster
========================================================

Functions
---------

`asyncio(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> Any | blaxel.models.private_cluster.PrivateCluster | None`
:   Delete private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`asyncio_detailed(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | blaxel.models.private_cluster.PrivateCluster]`
:   Delete private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]

`sync(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> Any | blaxel.models.private_cluster.PrivateCluster | None`
:   Delete private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`sync_detailed(private_cluster_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | blaxel.models.private_cluster.PrivateCluster]`
:   Delete private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]