Module blaxel.api.policies.delete_policy
========================================

Functions
---------

`asyncio(policy_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.policy.Policy | None`
:   Delete policy
    
     Deletes a policy by name.
    
    Args:
        policy_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`asyncio_detailed(policy_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Delete policy
    
     Deletes a policy by name.
    
    Args:
        policy_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]

`sync(policy_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.policy.Policy | None`
:   Delete policy
    
     Deletes a policy by name.
    
    Args:
        policy_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`sync_detailed(policy_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Delete policy
    
     Deletes a policy by name.
    
    Args:
        policy_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]