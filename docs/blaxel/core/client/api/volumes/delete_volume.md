Module blaxel.core.client.api.volumes.delete_volume
===================================================

Functions
---------

`asyncio(volume_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.volume.Volume | None`
:   Delete volume
    
     Deletes a volume by name.
    
    Args:
        volume_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Volume

`asyncio_detailed(volume_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.volume.Volume]`
:   Delete volume
    
     Deletes a volume by name.
    
    Args:
        volume_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Volume]

`sync(volume_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.volume.Volume | None`
:   Delete volume
    
     Deletes a volume by name.
    
    Args:
        volume_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Volume

`sync_detailed(volume_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.volume.Volume]`
:   Delete volume
    
     Deletes a volume by name.
    
    Args:
        volume_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Volume]