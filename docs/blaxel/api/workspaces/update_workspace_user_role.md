Module blaxel.api.workspaces.update_workspace_user_role
=======================================================

Functions
---------

`asyncio(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_user_role_body.UpdateWorkspaceUserRoleBody) ‑> Any | blaxel.models.workspace_user.WorkspaceUser | None`
:   Update user role in workspace
    
     Updates the role of a user in the workspace.
    
    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, WorkspaceUser]

`asyncio_detailed(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_user_role_body.UpdateWorkspaceUserRoleBody) ‑> blaxel.types.Response[Any | blaxel.models.workspace_user.WorkspaceUser]`
:   Update user role in workspace
    
     Updates the role of a user in the workspace.
    
    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, WorkspaceUser]]

`sync(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_user_role_body.UpdateWorkspaceUserRoleBody) ‑> Any | blaxel.models.workspace_user.WorkspaceUser | None`
:   Update user role in workspace
    
     Updates the role of a user in the workspace.
    
    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, WorkspaceUser]

`sync_detailed(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_user_role_body.UpdateWorkspaceUserRoleBody) ‑> blaxel.types.Response[Any | blaxel.models.workspace_user.WorkspaceUser]`
:   Update user role in workspace
    
     Updates the role of a user in the workspace.
    
    Args:
        sub_or_email (str):
        body (UpdateWorkspaceUserRoleBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, WorkspaceUser]]