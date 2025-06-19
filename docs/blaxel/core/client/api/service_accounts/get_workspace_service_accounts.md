Module blaxel.core.client.api.service_accounts.get_workspace_service_accounts
=============================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.get_workspace_service_accounts_response_200_item.GetWorkspaceServiceAccountsResponse200Item] | None`
:   Get workspace service accounts
    
     Returns a list of all service accounts in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['GetWorkspaceServiceAccountsResponse200Item']

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.get_workspace_service_accounts_response_200_item.GetWorkspaceServiceAccountsResponse200Item]]`
:   Get workspace service accounts
    
     Returns a list of all service accounts in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['GetWorkspaceServiceAccountsResponse200Item']]

`sync(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.get_workspace_service_accounts_response_200_item.GetWorkspaceServiceAccountsResponse200Item] | None`
:   Get workspace service accounts
    
     Returns a list of all service accounts in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['GetWorkspaceServiceAccountsResponse200Item']

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.get_workspace_service_accounts_response_200_item.GetWorkspaceServiceAccountsResponse200Item]]`
:   Get workspace service accounts
    
     Returns a list of all service accounts in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['GetWorkspaceServiceAccountsResponse200Item']]