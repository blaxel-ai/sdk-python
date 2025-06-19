Module blaxel.core.client.api.jobs.update_job
=============================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.models.job.Job | None`
:   Create or update job
    
     Update a job by name.
    
    Args:
        job_id (str):
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Create or update job
    
     Update a job by name.
    
    Args:
        job_id (str):
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]

`sync(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.models.job.Job | None`
:   Create or update job
    
     Update a job by name.
    
    Args:
        job_id (str):
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Create or update job
    
     Update a job by name.
    
    Args:
        job_id (str):
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]