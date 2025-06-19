Module blaxel.core.sandbox.client.api.process.get_process_identifier_logs
=========================================================================

Functions
---------

`asyncio(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_logs.ProcessLogs | None`
:   Get process logs
    
     Get the stdout and stderr output of a process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, ProcessLogs]

`asyncio_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_logs.ProcessLogs]`
:   Get process logs
    
     Get the stdout and stderr output of a process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, ProcessLogs]]

`sync(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_logs.ProcessLogs | None`
:   Get process logs
    
     Get the stdout and stderr output of a process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, ProcessLogs]

`sync_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_logs.ProcessLogs]`
:   Get process logs
    
     Get the stdout and stderr output of a process
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, ProcessLogs]]