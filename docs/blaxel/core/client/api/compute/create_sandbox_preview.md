Module blaxel.core.client.api.compute.create_sandbox_preview
============================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview.Preview) ‑> blaxel.core.client.models.preview.Preview | None`
:   Create Sandbox Preview
    
     Create a preview
    
    Args:
        sandbox_name (str):
        body (Preview): Preview of a Resource
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Preview

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview.Preview) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview.Preview]`
:   Create Sandbox Preview
    
     Create a preview
    
    Args:
        sandbox_name (str):
        body (Preview): Preview of a Resource
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Preview]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview.Preview) ‑> blaxel.core.client.models.preview.Preview | None`
:   Create Sandbox Preview
    
     Create a preview
    
    Args:
        sandbox_name (str):
        body (Preview): Preview of a Resource
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Preview

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview.Preview) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview.Preview]`
:   Create Sandbox Preview
    
     Create a preview
    
    Args:
        sandbox_name (str):
        body (Preview): Preview of a Resource
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Preview]