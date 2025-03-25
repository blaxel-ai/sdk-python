Module blaxel.api.service_accounts.create_api_key_for_service_account
=====================================================================

Functions
---------

`asyncio(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.create_api_key_for_service_account_body.CreateApiKeyForServiceAccountBody) ‑> blaxel.models.api_key.ApiKey | None`
:   Create API key for service account
    
     Creates an API key for a service account.
    
    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        ApiKey

`asyncio_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.create_api_key_for_service_account_body.CreateApiKeyForServiceAccountBody) ‑> blaxel.types.Response[blaxel.models.api_key.ApiKey]`
:   Create API key for service account
    
     Creates an API key for a service account.
    
    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[ApiKey]

`sync(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.create_api_key_for_service_account_body.CreateApiKeyForServiceAccountBody) ‑> blaxel.models.api_key.ApiKey | None`
:   Create API key for service account
    
     Creates an API key for a service account.
    
    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        ApiKey

`sync_detailed(client_id: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.create_api_key_for_service_account_body.CreateApiKeyForServiceAccountBody) ‑> blaxel.types.Response[blaxel.models.api_key.ApiKey]`
:   Create API key for service account
    
     Creates an API key for a service account.
    
    Args:
        client_id (str):
        body (CreateApiKeyForServiceAccountBody):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[ApiKey]