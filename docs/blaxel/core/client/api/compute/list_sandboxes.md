Module blaxel.core.client.api.compute.list_sandboxes
====================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.sandbox.Sandbox] | None`
:   List Sandboxes
    
     Returns a list of all Sandboxes in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Sandbox']

`asyncio_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.sandbox.Sandbox]]`
:   List Sandboxes
    
     Returns a list of all Sandboxes in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Sandbox']]

`sync(*, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.sandbox.Sandbox] | None`
:   List Sandboxes
    
     Returns a list of all Sandboxes in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Sandbox']

`sync_detailed(*, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.sandbox.Sandbox]]`
:   List Sandboxes
    
     Returns a list of all Sandboxes in the workspace.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Sandbox']]