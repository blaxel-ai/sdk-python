Module blaxel.api.functions.list_function_revisions
===================================================

Functions
---------

`asyncio(function_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List function revisions
    
     Returns revisions for a function by name.
    
    Args:
        function_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`asyncio_detailed(function_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List function revisions
    
     Returns revisions for a function by name.
    
    Args:
        function_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]

`sync(function_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List function revisions
    
     Returns revisions for a function by name.
    
    Args:
        function_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`sync_detailed(function_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List function revisions
    
     Returns revisions for a function by name.
    
    Args:
        function_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]