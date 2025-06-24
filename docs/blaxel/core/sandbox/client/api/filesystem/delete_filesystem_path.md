Module blaxel.core.sandbox.client.api.filesystem.delete_filesystem_path
=======================================================================

Functions
---------

`asyncio(path: str, *, client: blaxel.core.sandbox.client.client.Client, recursive: blaxel.core.sandbox.client.types.Unset | bool = <blaxel.core.sandbox.client.types.Unset object>) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Delete file or directory
    
     Delete a file or directory
    
    Args:
        path (str):
        recursive (Union[Unset, bool]):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`asyncio_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client, recursive: blaxel.core.sandbox.client.types.Unset | bool = <blaxel.core.sandbox.client.types.Unset object>) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Delete file or directory
    
     Delete a file or directory
    
    Args:
        path (str):
        recursive (Union[Unset, bool]):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]

`sync(path: str, *, client: blaxel.core.sandbox.client.client.Client, recursive: blaxel.core.sandbox.client.types.Unset | bool = <blaxel.core.sandbox.client.types.Unset object>) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse | None`
:   Delete file or directory
    
     Delete a file or directory
    
    Args:
        path (str):
        recursive (Union[Unset, bool]):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, SuccessResponse]

`sync_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client, recursive: blaxel.core.sandbox.client.types.Unset | bool = <blaxel.core.sandbox.client.types.Unset object>) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.success_response.SuccessResponse]`
:   Delete file or directory
    
     Delete a file or directory
    
    Args:
        path (str):
        recursive (Union[Unset, bool]):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, SuccessResponse]]