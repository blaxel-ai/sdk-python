Module blaxel.core.client.api.jobs.get_job
==========================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.model.Model | None`
:   Get job
    
     Returns a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Get job
    
     Returns a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]

`sync(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.model.Model | None`
:   Get job
    
     Returns a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Get job
    
     Returns a job by name.
    
    Args:
        job_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]