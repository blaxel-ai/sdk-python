Module blaxel.core.client.api.jobs.create_job
=============================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.models.job.Job | None`
:   Create job
    
     Creates a job.
    
    Args:
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Create job
    
     Creates a job.
    
    Args:
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.models.job.Job | None`
:   Create job
    
     Creates a job.
    
    Args:
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Job

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.job.Job) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.job.Job]`
:   Create job
    
     Creates a job.
    
    Args:
        body (Job): Job
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Job]