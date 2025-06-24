Module blaxel.core.client.api.compute.create_sandbox
====================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Create Sandbox
    
     Creates a Sandbox.
    
    Args:
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Create Sandbox
    
     Creates a Sandbox.
    
    Args:
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.models.sandbox.Sandbox | None`
:   Create Sandbox
    
     Creates a Sandbox.
    
    Args:
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Sandbox

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.sandbox.Sandbox]`
:   Create Sandbox
    
     Creates a Sandbox.
    
    Args:
        body (Sandbox): Micro VM for running agentic tasks
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Sandbox]