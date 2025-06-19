Module blaxel.core.client.api.compute.update_sandbox
====================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Update Sandbox
    
     Update a Sandbox by name.
    
    Args:
        sandbox_name (str):
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Update Sandbox
    
     Update a Sandbox by name.
    
    Args:
        sandbox_name (str):
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Update Sandbox
    
     Update a Sandbox by name.
    
    Args:
        sandbox_name (str):
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Update Sandbox
    
     Update a Sandbox by name.
    
    Args:
        sandbox_name (str):
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]