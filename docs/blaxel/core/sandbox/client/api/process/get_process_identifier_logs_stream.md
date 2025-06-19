Module blaxel.core.sandbox.client.api.process.get_process_identifier_logs_stream
================================================================================

Functions
---------

`asyncio(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | str | None`
:   Stream process logs in real time
    
     Streams the stdout and stderr output of a process in real time, one line per log, prefixed with
    'stdout:' or 'stderr:'. Closes when the process exits or the client disconnects.
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, str]

`asyncio_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | str]`
:   Stream process logs in real time
    
     Streams the stdout and stderr output of a process in real time, one line per log, prefixed with
    'stdout:' or 'stderr:'. Closes when the process exits or the client disconnects.
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, str]]

`sync(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | str | None`
:   Stream process logs in real time
    
     Streams the stdout and stderr output of a process in real time, one line per log, prefixed with
    'stdout:' or 'stderr:'. Closes when the process exits or the client disconnects.
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, str]

`sync_detailed(identifier: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | str]`
:   Stream process logs in real time
    
     Streams the stdout and stderr output of a process in real time, one line per log, prefixed with
    'stdout:' or 'stderr:'. Closes when the process exits or the client disconnects.
    
    Args:
        identifier (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, str]]