Module blaxel.core.client.api.compute.stop_sandbox
==================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.stop_sandbox.StopSandbox | None`
:   Stop Sandbox
    
     Stops a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, StopSandbox]

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.stop_sandbox.StopSandbox]`
:   Stop Sandbox
    
     Stops a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, StopSandbox]]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.stop_sandbox.StopSandbox | None`
:   Stop Sandbox
    
     Stops a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, StopSandbox]

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.stop_sandbox.StopSandbox]`
:   Stop Sandbox
    
     Stops a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, StopSandbox]]