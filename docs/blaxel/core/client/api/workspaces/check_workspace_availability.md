Module blaxel.core.client.api.workspaces.check_workspace_availability
=====================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.check_workspace_availability_body.CheckWorkspaceAvailabilityBody) ‑> bool | None`
:   Check workspace availability
    
     Check if a workspace is available.
    
    Args:
        body (CheckWorkspaceAvailabilityBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        bool

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.check_workspace_availability_body.CheckWorkspaceAvailabilityBody) ‑> blaxel.core.client.types.Response[bool]`
:   Check workspace availability
    
     Check if a workspace is available.
    
    Args:
        body (CheckWorkspaceAvailabilityBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[bool]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.check_workspace_availability_body.CheckWorkspaceAvailabilityBody) ‑> bool | None`
:   Check workspace availability
    
     Check if a workspace is available.
    
    Args:
        body (CheckWorkspaceAvailabilityBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        bool

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.check_workspace_availability_body.CheckWorkspaceAvailabilityBody) ‑> blaxel.core.client.types.Response[bool]`
:   Check workspace availability
    
     Check if a workspace is available.
    
    Args:
        body (CheckWorkspaceAvailabilityBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[bool]