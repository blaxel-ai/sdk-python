Module blaxel.core.client.api.workspaces.delete_workspace
=========================================================

Functions
---------

`asyncio(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.workspace.Workspace | None`
:   Delete workspace
    
     Deletes a workspace by name.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Workspace

`asyncio_detailed(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.workspace.Workspace]`
:   Delete workspace
    
     Deletes a workspace by name.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Workspace]

`sync(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.workspace.Workspace | None`
:   Delete workspace
    
     Deletes a workspace by name.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Workspace

`sync_detailed(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.workspace.Workspace]`
:   Delete workspace
    
     Deletes a workspace by name.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Workspace]