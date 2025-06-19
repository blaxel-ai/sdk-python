Module blaxel.core.client.api.compute.delete_sandbox_preview_token
==================================================================

Functions
---------

`asyncio(sandbox_name: str, preview_name: str, token_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.delete_sandbox_preview_token_response_200.DeleteSandboxPreviewTokenResponse200 | None`
:   Delete token for Sandbox Preview
    
     Deletes a token for a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        DeleteSandboxPreviewTokenResponse200

`asyncio_detailed(sandbox_name: str, preview_name: str, token_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.delete_sandbox_preview_token_response_200.DeleteSandboxPreviewTokenResponse200]`
:   Delete token for Sandbox Preview
    
     Deletes a token for a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[DeleteSandboxPreviewTokenResponse200]

`sync(sandbox_name: str, preview_name: str, token_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.delete_sandbox_preview_token_response_200.DeleteSandboxPreviewTokenResponse200 | None`
:   Delete token for Sandbox Preview
    
     Deletes a token for a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        DeleteSandboxPreviewTokenResponse200

`sync_detailed(sandbox_name: str, preview_name: str, token_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.delete_sandbox_preview_token_response_200.DeleteSandboxPreviewTokenResponse200]`
:   Delete token for Sandbox Preview
    
     Deletes a token for a Sandbox Preview by name.
    
    Args:
        sandbox_name (str):
        preview_name (str):
        token_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[DeleteSandboxPreviewTokenResponse200]