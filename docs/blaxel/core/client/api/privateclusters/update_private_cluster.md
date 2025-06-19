Module blaxel.core.client.api.privateclusters.update_private_cluster
====================================================================

Functions
---------

`asyncio(private_cluster_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.private_cluster.PrivateCluster | None`
:   Update private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`asyncio_detailed(private_cluster_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.private_cluster.PrivateCluster]`
:   Update private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]

`sync(private_cluster_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.private_cluster.PrivateCluster | None`
:   Update private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`sync_detailed(private_cluster_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.private_cluster.PrivateCluster]`
:   Update private cluster
    
    Args:
        private_cluster_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]