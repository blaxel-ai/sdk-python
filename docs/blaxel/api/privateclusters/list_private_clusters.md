Module blaxel.api.privateclusters.list_private_clusters
=======================================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> Any | list[blaxel.models.private_cluster.PrivateCluster] | None`
:   List all private clusters
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['PrivateCluster']]

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | list[blaxel.models.private_cluster.PrivateCluster]]`
:   List all private clusters
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['PrivateCluster']]]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> Any | list[blaxel.models.private_cluster.PrivateCluster] | None`
:   List all private clusters
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['PrivateCluster']]

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | list[blaxel.models.private_cluster.PrivateCluster]]`
:   List all private clusters
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['PrivateCluster']]]