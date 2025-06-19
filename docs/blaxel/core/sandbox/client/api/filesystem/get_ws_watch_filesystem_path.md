Module blaxel.core.sandbox.client.api.filesystem.get_ws_watch_filesystem_path
=============================================================================

Functions
---------

`asyncio(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | str | None`
:   Stream file modification events in a directory via WebSocket
    
     Streams JSON events of modified files in the given directory. Closes when the client disconnects.
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, str]

`asyncio_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | str]`
:   Stream file modification events in a directory via WebSocket
    
     Streams JSON events of modified files in the given directory. Closes when the client disconnects.
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, str]]

`sync(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | str | None`
:   Stream file modification events in a directory via WebSocket
    
     Streams JSON events of modified files in the given directory. Closes when the client disconnects.
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, str]

`sync_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | str]`
:   Stream file modification events in a directory via WebSocket
    
     Streams JSON events of modified files in the given directory. Closes when the client disconnects.
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, str]]