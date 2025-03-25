Module blaxel.api.functions.create_function
===========================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.models.function.Function | None`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.types.Response[blaxel.models.function.Function]`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]

`sync(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.models.function.Function | None`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`sync_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.types.Response[blaxel.models.function.Function]`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]