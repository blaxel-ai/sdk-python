Module blaxel.core.sandbox.client.api.process.post_process
==========================================================

Functions
---------

`asyncio(*, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.process_request.ProcessRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_response.ProcessResponse | None`
:   Execute a command
    
     Execute a command and return process information
    
    Args:
        body (ProcessRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, ProcessResponse]

`asyncio_detailed(*, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.process_request.ProcessRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_response.ProcessResponse]`
:   Execute a command
    
     Execute a command and return process information
    
    Args:
        body (ProcessRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, ProcessResponse]]

`sync(*, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.process_request.ProcessRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_response.ProcessResponse | None`
:   Execute a command
    
     Execute a command and return process information
    
    Args:
        body (ProcessRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, ProcessResponse]

`sync_detailed(*, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.process_request.ProcessRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.process_response.ProcessResponse]`
:   Execute a command
    
     Execute a command and return process information
    
    Args:
        body (ProcessRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, ProcessResponse]]