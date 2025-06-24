Module blaxel.core.client.api.policies.create_policy
====================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.policy.Policy) ‑> blaxel.core.client.models.policy.Policy | None`
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

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.policy.Policy) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.policy.Policy]`
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

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.policy.Policy) ‑> blaxel.core.client.models.policy.Policy | None`
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

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.policy.Policy) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.policy.Policy]`
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