Module blaxel.core.client.api.privateclusters.create_private_cluster
====================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.private_cluster.PrivateCluster | None`
:   Create private cluster
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.private_cluster.PrivateCluster]`
:   Create private cluster
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]

`sync(*, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.private_cluster.PrivateCluster | None`
:   Create private cluster
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, PrivateCluster]

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.private_cluster.PrivateCluster]`
:   Create private cluster
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, PrivateCluster]]