Module blaxel.core.client.api.service_accounts.create_workspace_service_account
===============================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_workspace_service_account_body.CreateWorkspaceServiceAccountBody) ‑> blaxel.core.client.models.create_workspace_service_account_response_200.CreateWorkspaceServiceAccountResponse200 | None`
:   Create workspace service account
    
     Creates a service account in the workspace.
    
    Args:
        body (CreateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CreateWorkspaceServiceAccountResponse200

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_workspace_service_account_body.CreateWorkspaceServiceAccountBody) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.create_workspace_service_account_response_200.CreateWorkspaceServiceAccountResponse200]`
:   Create workspace service account
    
     Creates a service account in the workspace.
    
    Args:
        body (CreateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CreateWorkspaceServiceAccountResponse200]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_workspace_service_account_body.CreateWorkspaceServiceAccountBody) ‑> blaxel.core.client.models.create_workspace_service_account_response_200.CreateWorkspaceServiceAccountResponse200 | None`
:   Create workspace service account
    
     Creates a service account in the workspace.
    
    Args:
        body (CreateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CreateWorkspaceServiceAccountResponse200

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_workspace_service_account_body.CreateWorkspaceServiceAccountBody) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.create_workspace_service_account_response_200.CreateWorkspaceServiceAccountResponse200]`
:   Create workspace service account
    
     Creates a service account in the workspace.
    
    Args:
        body (CreateWorkspaceServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CreateWorkspaceServiceAccountResponse200]