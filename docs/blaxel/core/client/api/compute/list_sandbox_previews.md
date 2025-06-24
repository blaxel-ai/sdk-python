Module blaxel.core.client.api.compute.list_sandbox_previews
===========================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.preview.Preview] | None`
:   List Sandboxes
    
     Returns a list of Sandbox Previews in the workspace.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Preview']

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.preview.Preview]]`
:   List Sandboxes
    
     Returns a list of Sandbox Previews in the workspace.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Preview']]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.preview.Preview] | None`
:   List Sandboxes
    
     Returns a list of Sandbox Previews in the workspace.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Preview']

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.preview.Preview]]`
:   List Sandboxes
    
     Returns a list of Sandbox Previews in the workspace.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Preview']]