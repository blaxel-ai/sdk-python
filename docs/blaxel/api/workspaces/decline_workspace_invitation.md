Module blaxel.api.workspaces.decline_workspace_invitation
=========================================================

Functions
---------

`asyncio(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.pending_invitation.PendingInvitation | None`
:   Decline invitation to workspace
    
     Declines an invitation to a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PendingInvitation

`asyncio_detailed(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.pending_invitation.PendingInvitation]`
:   Decline invitation to workspace
    
     Declines an invitation to a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PendingInvitation]

`sync(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.pending_invitation.PendingInvitation | None`
:   Decline invitation to workspace
    
     Declines an invitation to a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        PendingInvitation

`sync_detailed(workspace_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.pending_invitation.PendingInvitation]`
:   Decline invitation to workspace
    
     Declines an invitation to a workspace.
    
    Args:
        workspace_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[PendingInvitation]