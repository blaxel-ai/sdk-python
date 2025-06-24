Module blaxel.core.client.api.compute.delete_sandbox_preview
============================================================

Functions
---------

`asyncio(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.preview.Preview | None`
:   Delete Sandbox Preview
    
     Deletes a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Preview

`asyncio_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview.Preview]`
:   Delete Sandbox Preview
    
     Deletes a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Preview]

`sync(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.preview.Preview | None`
:   Delete Sandbox Preview
    
     Deletes a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Preview

`sync_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview.Preview]`
:   Delete Sandbox Preview
    
     Deletes a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Preview]