Module blaxel.api.models.list_model_revisions
=============================================

Functions
---------

`asyncio(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`asyncio_detailed(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]

`sync(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`sync_detailed(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]