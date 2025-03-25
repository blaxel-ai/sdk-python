Module blaxel.api.service_accounts.delete_api_key_for_service_account
=====================================================================

Functions
---------

`asyncio_detailed(client_id: str, api_key_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Delete API key for service account
    
     Deletes an API key for a service account.
    
    Args:
        client_id (str):
        api_key_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]

`sync_detailed(client_id: str, api_key_id: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[typing.Any]`
:   Delete API key for service account
    
     Deletes an API key for a service account.
    
    Args:
        client_id (str):
        api_key_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Any]