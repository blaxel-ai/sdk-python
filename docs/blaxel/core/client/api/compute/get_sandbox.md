Module blaxel.core.client.api.compute.get_sandbox
=================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Get Sandbox
    
     Returns a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Get Sandbox
    
     Returns a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Get Sandbox
    
     Returns a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Get Sandbox
    
     Returns a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]