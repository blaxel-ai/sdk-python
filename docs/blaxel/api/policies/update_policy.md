Module blaxel.api.policies.update_policy
========================================

Functions
---------

`asyncio(policy_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.models.policy.Policy | None`
:   Update policy
    
     Updates a policy.
    
    Args:
        policy_name (str):
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`asyncio_detailed(policy_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Update policy
    
     Updates a policy.
    
    Args:
        policy_name (str):
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]

`sync(policy_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.models.policy.Policy | None`
:   Update policy
    
     Updates a policy.
    
    Args:
        policy_name (str):
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`sync_detailed(policy_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Update policy
    
     Updates a policy.
    
    Args:
        policy_name (str):
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]