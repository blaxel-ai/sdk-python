Module blaxel.api.policies.create_policy
========================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.models.policy.Policy | None`
:   Create policy
    
     Creates a policy.
    
    Args:
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Create policy
    
     Creates a policy.
    
    Args:
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]

`sync(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.models.policy.Policy | None`
:   Create policy
    
     Creates a policy.
    
    Args:
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Policy

`sync_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.policy.Policy) ‑> blaxel.types.Response[blaxel.models.policy.Policy]`
:   Create policy
    
     Creates a policy.
    
    Args:
        body (Policy): Rule that controls how a deployment is made and served (e.g. location
            restrictions)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Policy]