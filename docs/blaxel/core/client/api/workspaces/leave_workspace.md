Module blaxel.core.client.api.workspaces.leave_workspace
========================================================

Functions
---------

`asyncio(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.workspace.Workspace | None`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, Workspace]

`asyncio_detailed(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.workspace.Workspace]`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, Workspace]]

`sync(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.workspace.Workspace | None`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, Workspace]

`sync_detailed(workspace_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.workspace.Workspace]`
:   Leave workspace
    
     Leaves a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, Workspace]]