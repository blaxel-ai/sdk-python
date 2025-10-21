Module blaxel.core.client.api.volumes.create_volume
===================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.volume.Volume) ‑> blaxel.core.client.models.volume.Volume | None`
:   Create volume
    
     Creates a volume.
    
    Args:
        body (Volume): Volume resource for persistent storage
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Volume

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.volume.Volume) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.volume.Volume]`
:   Create volume
    
     Creates a volume.
    
    Args:
        body (Volume): Volume resource for persistent storage
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Volume]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.volume.Volume) ‑> blaxel.core.client.models.volume.Volume | None`
:   Create volume
    
     Creates a volume.
    
    Args:
        body (Volume): Volume resource for persistent storage
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Volume

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.volume.Volume) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.volume.Volume]`
:   Create volume
    
     Creates a volume.
    
    Args:
        body (Volume): Volume resource for persistent storage
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Volume]