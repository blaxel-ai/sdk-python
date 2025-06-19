Module blaxel.core.client.api.compute.create_sandbox_preview_token
==================================================================

Functions
---------

`asyncio(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview_token.PreviewToken) ‑> blaxel.core.client.models.preview_token.PreviewToken | None`
:   Create token for Sandbox Preview
    
     Creates a token for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        body (PreviewToken): Token for a Preview
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PreviewToken

`asyncio_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview_token.PreviewToken) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview_token.PreviewToken]`
:   Create token for Sandbox Preview
    
     Creates a token for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        body (PreviewToken): Token for a Preview
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PreviewToken]

`sync(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview_token.PreviewToken) ‑> blaxel.core.client.models.preview_token.PreviewToken | None`
:   Create token for Sandbox Preview
    
     Creates a token for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        body (PreviewToken): Token for a Preview
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PreviewToken

`sync_detailed(sandbox_name: str, preview_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.preview_token.PreviewToken) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.preview_token.PreviewToken]`
:   Create token for Sandbox Preview
    
     Creates a token for a Sandbox Preview.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        body (PreviewToken): Token for a Preview
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PreviewToken]