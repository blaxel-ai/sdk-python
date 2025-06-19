Module blaxel.core.sandbox.client.api.filesystem.put_filesystem_path
====================================================================

Functions
---------

`asyncio(path: str, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.file_request.FileRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Create or update a file or directory
    
     Create or update a file or directory
    
    Args:
        path (str):
        body (FileRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`asyncio_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.file_request.FileRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Create or update a file or directory
    
     Create or update a file or directory
    
    Args:
        path (str):
        body (FileRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]

`sync(path: str, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.file_request.FileRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Create or update a file or directory
    
     Create or update a file or directory
    
    Args:
        path (str):
        body (FileRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`sync_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.file_request.FileRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Create or update a file or directory
    
     Create or update a file or directory
    
    Args:
        path (str):
        body (FileRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]