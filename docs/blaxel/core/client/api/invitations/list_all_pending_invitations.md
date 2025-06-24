Module blaxel.core.client.api.invitations.list_all_pending_invitations
======================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> Any | list[blaxel.core.client.models.pending_invitation_render.PendingInvitationRender] | None`
:   List pending invitations
    
     Returns a list of all pending invitations in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['PendingInvitationRender']]

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | list[blaxel.core.client.models.pending_invitation_render.PendingInvitationRender]]`
:   List pending invitations
    
     Returns a list of all pending invitations in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['PendingInvitationRender']]]

`sync(*, client: blaxel.core.client.client.Client) ‑> Any | list[blaxel.core.client.models.pending_invitation_render.PendingInvitationRender] | None`
:   List pending invitations
    
     Returns a list of all pending invitations in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['PendingInvitationRender']]

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | list[blaxel.core.client.models.pending_invitation_render.PendingInvitationRender]]`
:   List pending invitations
    
     Returns a list of all pending invitations in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['PendingInvitationRender']]]