Module blaxel.api.knowledgebases.list_knowledgebase_revisions
=============================================================

Functions
---------

`asyncio(knowledgebase_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List knowledgebase revisions
    
     Returns revisions for a knowledgebase by name.
    
    Args:
        knowledgebase_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`asyncio_detailed(knowledgebase_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List knowledgebase revisions
    
     Returns revisions for a knowledgebase by name.
    
    Args:
        knowledgebase_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]

`sync(knowledgebase_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.revision_metadata.RevisionMetadata | None`
:   List knowledgebase revisions
    
     Returns revisions for a knowledgebase by name.
    
    Args:
        knowledgebase_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        RevisionMetadata

`sync_detailed(knowledgebase_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.revision_metadata.RevisionMetadata]`
:   List knowledgebase revisions
    
     Returns revisions for a knowledgebase by name.
    
    Args:
        knowledgebase_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[RevisionMetadata]