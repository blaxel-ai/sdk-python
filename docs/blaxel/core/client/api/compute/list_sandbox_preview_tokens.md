Module blaxel.core.client.api.compute.list_sandbox_preview_tokens
=================================================================

Functions
---------

`asyncio(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.preview_token.PreviewToken] | None`
:   Get tokens for Sandbox Preview
    
     Gets tokens for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['PreviewToken']

`asyncio_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.preview_token.PreviewToken]]`
:   Get tokens for Sandbox Preview
    
     Gets tokens for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['PreviewToken']]

`sync(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.preview_token.PreviewToken] | None`
:   Get tokens for Sandbox Preview
    
     Gets tokens for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['PreviewToken']

`sync_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.preview_token.PreviewToken]]`
:   Get tokens for Sandbox Preview
    
     Gets tokens for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['PreviewToken']]