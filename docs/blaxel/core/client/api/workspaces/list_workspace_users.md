Module blaxel.core.client.api.workspaces.list_workspace_users
=============================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.workspace_user.WorkspaceUser] | None`
:   List users in workspace
    
     Returns a list of all users in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['WorkspaceUser']

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.workspace_user.WorkspaceUser]]`
:   List users in workspace
    
     Returns a list of all users in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['WorkspaceUser']]

`sync(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.workspace_user.WorkspaceUser] | None`
:   List users in workspace
    
     Returns a list of all users in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['WorkspaceUser']

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.workspace_user.WorkspaceUser]]`
:   List users in workspace
    
     Returns a list of all users in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['WorkspaceUser']]