Module blaxel.core.client.api.compute.start_sandbox
===================================================

Functions
---------

`asyncio(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.start_sandbox.StartSandbox | None`
:   Start Sandbox
    
     Starts a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, StartSandbox]

`asyncio_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.start_sandbox.StartSandbox]`
:   Start Sandbox
    
     Starts a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, StartSandbox]]

`sync(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.start_sandbox.StartSandbox | None`
:   Start Sandbox
    
     Starts a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, StartSandbox]

`sync_detailed(sandbox_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.start_sandbox.StartSandbox]`
:   Start Sandbox
    
     Starts a Sandbox by name.
    
    Args:
        sandbox_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, StartSandbox]]