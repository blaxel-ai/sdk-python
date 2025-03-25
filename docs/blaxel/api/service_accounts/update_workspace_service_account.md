Module blaxel.api.service_accounts.update_workspace_service_account
===================================================================

Functions
---------

`asyncio(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_service_account_body.UpdateWorkspaceServiceAccountBody) ‑> blaxel.models.update_workspace_service_account_response_200.UpdateWorkspaceServiceAccountResponse200 | None`
:   Update workspace service account
    
     Updates a service account.
    
    Args:
        client_id (str):
        body (UpdateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        UpdateWorkspaceServiceAccountResponse200

`asyncio_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_service_account_body.UpdateWorkspaceServiceAccountBody) ‑> blaxel.types.Response[blaxel.models.update_workspace_service_account_response_200.UpdateWorkspaceServiceAccountResponse200]`
:   Update workspace service account
    
     Updates a service account.
    
    Args:
        client_id (str):
        body (UpdateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[UpdateWorkspaceServiceAccountResponse200]

`sync(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_service_account_body.UpdateWorkspaceServiceAccountBody) ‑> blaxel.models.update_workspace_service_account_response_200.UpdateWorkspaceServiceAccountResponse200 | None`
:   Update workspace service account
    
     Updates a service account.
    
    Args:
        client_id (str):
        body (UpdateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        UpdateWorkspaceServiceAccountResponse200

`sync_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.update_workspace_service_account_body.UpdateWorkspaceServiceAccountBody) ‑> blaxel.types.Response[blaxel.models.update_workspace_service_account_response_200.UpdateWorkspaceServiceAccountResponse200]`
:   Update workspace service account
    
     Updates a service account.
    
    Args:
        client_id (str):
        body (UpdateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[UpdateWorkspaceServiceAccountResponse200]