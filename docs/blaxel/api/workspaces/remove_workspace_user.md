Module blaxel.api.workspaces.remove_workspace_user
==================================================

Functions
---------

`asyncio_detailed(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Remove user from workspace or revoke invitation
    
     Removes a user from the workspace (or revokes an invitation if the user has not accepted the
    invitation yet).
    
    Args:
        sub_or_email (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(sub_or_email: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Remove user from workspace or revoke invitation
    
     Removes a user from the workspace (or revokes an invitation if the user has not accepted the
    invitation yet).
    
    Args:
        sub_or_email (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]