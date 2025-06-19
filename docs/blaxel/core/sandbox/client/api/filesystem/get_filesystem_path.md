Module blaxel.core.sandbox.client.api.filesystem.get_filesystem_path
====================================================================

Functions
---------

`asyncio(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.directory.Directory | blaxel.core.sandbox.client.models.file_with_content.FileWithContent | None`
:   Get file or directory information
    
     Get content of a file or listing of a directory
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, Union['Directory', 'FileWithContent']]

`asyncio_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.directory.Directory | blaxel.core.sandbox.client.models.file_with_content.FileWithContent]`
:   Get file or directory information
    
     Get content of a file or listing of a directory
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, Union['Directory', 'FileWithContent']]]

`sync(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.directory.Directory | blaxel.core.sandbox.client.models.file_with_content.FileWithContent | None`
:   Get file or directory information
    
     Get content of a file or listing of a directory
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, Union['Directory', 'FileWithContent']]

`sync_detailed(path: str, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.directory.Directory | blaxel.core.sandbox.client.models.file_with_content.FileWithContent]`
:   Get file or directory information
    
     Get content of a file or listing of a directory
    
    Args:
        path (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, Union['Directory', 'FileWithContent']]]