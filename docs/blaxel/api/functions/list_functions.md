Module blaxel.api.functions.list_functions
==========================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.function.Function] | None`
:   List all functions
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Function']

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.function.Function]]`
:   List all functions
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Function']]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.function.Function] | None`
:   List all functions
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Function']

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.function.Function]]`
:   List all functions
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Function']]