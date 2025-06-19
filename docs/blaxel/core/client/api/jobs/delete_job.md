Module blaxel.core.client.api.jobs.delete_job
=============================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.job.Job | None`
:   Delete job
    
     Deletes a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Delete job
    
     Deletes a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]

`sync(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.job.Job | None`
:   Delete job
    
     Deletes a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Delete job
    
     Deletes a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]