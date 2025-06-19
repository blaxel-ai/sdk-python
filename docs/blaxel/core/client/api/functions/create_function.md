Module blaxel.core.client.api.functions.create_function
=======================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.function.Function) ‑> blaxel.core.client.models.function.Function | None`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.function.Function) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.function.Function]`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.function.Function) ‑> blaxel.core.client.models.function.Function | None`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.function.Function) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.function.Function]`
:   Create function
    
    Args:
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]