Module blaxel.api.service_accounts.delete_workspace_service_account
===================================================================

Functions
---------

`asyncio(client_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.delete_workspace_service_account_response_200.DeleteWorkspaceServiceAccountResponse200 | None`
:   Delete workspace service account
    
     Deletes a service account.
    
    Args:
        client_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        DeleteWorkspaceServiceAccountResponse200

`asyncio_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.delete_workspace_service_account_response_200.DeleteWorkspaceServiceAccountResponse200]`
:   Delete workspace service account
    
     Deletes a service account.
    
    Args:
        client_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[DeleteWorkspaceServiceAccountResponse200]

`sync(client_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.delete_workspace_service_account_response_200.DeleteWorkspaceServiceAccountResponse200 | None`
:   Delete workspace service account
    
     Deletes a service account.
    
    Args:
        client_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        DeleteWorkspaceServiceAccountResponse200

`sync_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.delete_workspace_service_account_response_200.DeleteWorkspaceServiceAccountResponse200]`
:   Delete workspace service account
    
     Deletes a service account.
    
    Args:
        client_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[DeleteWorkspaceServiceAccountResponse200]