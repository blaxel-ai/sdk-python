Module blaxel.api.functions.update_function
===========================================

Functions
---------

`asyncio(function_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.models.function.Function | None`
:   Update function by name
    
    Args:
        function_name (str):
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`asyncio_detailed(function_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.types.Response[blaxel.models.function.Function]`
:   Update function by name
    
    Args:
        function_name (str):
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]

`sync(function_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.models.function.Function | None`
:   Update function by name
    
    Args:
        function_name (str):
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Function

`sync_detailed(function_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.function.Function) ‑> blaxel.types.Response[blaxel.models.function.Function]`
:   Update function by name
    
    Args:
        function_name (str):
        body (Function): Function
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Function]