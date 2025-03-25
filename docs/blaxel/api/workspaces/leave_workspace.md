Module blaxel.api.workspaces.leave_workspace
============================================

Functions
---------

`asyncio(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> Any | blaxel.models.workspace.Workspace | None`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, Workspace]

`asyncio_detailed(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | blaxel.models.workspace.Workspace]`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, Workspace]]

`sync(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> Any | blaxel.models.workspace.Workspace | None`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, Workspace]

`sync_detailed(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[Any | blaxel.models.workspace.Workspace]`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, Workspace]]