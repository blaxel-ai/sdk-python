Module blaxel.core.client.api.workspaces.create_worspace
========================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.workspace.Workspace) ‑> blaxel.core.client.models.workspace.Workspace | None`
:   Create worspace
    
     Creates a workspace.
    
    Args:
        body (Workspace): Workspace
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Workspace

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.workspace.Workspace) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.workspace.Workspace]`
:   Create worspace
    
     Creates a workspace.
    
    Args:
        body (Workspace): Workspace
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Workspace]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.workspace.Workspace) ‑> blaxel.core.client.models.workspace.Workspace | None`
:   Create worspace
    
     Creates a workspace.
    
    Args:
        body (Workspace): Workspace
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Workspace

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.workspace.Workspace) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.workspace.Workspace]`
:   Create worspace
    
     Creates a workspace.
    
    Args:
        body (Workspace): Workspace
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Workspace]