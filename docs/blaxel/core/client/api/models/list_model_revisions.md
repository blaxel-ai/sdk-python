Module blaxel.core.client.api.models.list_model_revisions
=========================================================

Functions
---------

`asyncio(model_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.revision_metadata.RevisionMetadata] | None`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`asyncio_detailed(model_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.revision_metadata.RevisionMetadata]]`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]

`sync(model_name: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.revision_metadata.RevisionMetadata] | None`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`sync_detailed(model_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.revision_metadata.RevisionMetadata]]`
:   List model revisions
    
     Returns revisions for a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]