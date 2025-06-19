Module blaxel.core.client.api.jobs.list_job_revisions
=====================================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.revision_metadata.RevisionMetadata] | None`
:   List job revisions
    
     Returns revisions for a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.revision_metadata.RevisionMetadata]]`
:   List job revisions
    
     Returns revisions for a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]

`sync(job_id: str, *, client: blaxel.core.client.client.Client) ‑> list[blaxel.core.client.models.revision_metadata.RevisionMetadata] | None`
:   List job revisions
    
     Returns revisions for a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[list[blaxel.core.client.models.revision_metadata.RevisionMetadata]]`
:   List job revisions
    
     Returns revisions for a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]