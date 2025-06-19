Module blaxel.core.client.api.workspaces.list_workspaces
========================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.workspace.Workspace] | None`
:   List workspaces
    
     Returns a list of all workspaces.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Workspace']

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.workspace.Workspace]]`
:   List workspaces
    
     Returns a list of all workspaces.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Workspace']]

`sync(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.workspace.Workspace] | None`
:   List workspaces
    
     Returns a list of all workspaces.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Workspace']

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.workspace.Workspace]]`
:   List workspaces
    
     Returns a list of all workspaces.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Workspace']]