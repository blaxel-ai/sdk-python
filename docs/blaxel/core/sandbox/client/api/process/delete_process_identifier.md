Module blaxel.core.sandbox.client.api.process.delete_process_identifier
=======================================================================

Functions
---------

`asyncio(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Stop a process
    
     Gracefully stop a running process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`asyncio_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Stop a process
    
     Gracefully stop a running process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]

`sync(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Stop a process
    
     Gracefully stop a running process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`sync_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Stop a process
    
     Gracefully stop a running process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]