Module blaxel.core.client.api.jobs.get_job_execution
====================================================

Functions
---------

`asyncio(job_id: str, execution_id: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.job_execution.JobExecution | None`
:   Get job execution
    
     Returns an execution for a job by name.
    
    Args:
        job_id (str):
        execution_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, JobExecution]

`asyncio_detailed(job_id: str, execution_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.job_execution.JobExecution]`
:   Get job execution
    
     Returns an execution for a job by name.
    
    Args:
        job_id (str):
        execution_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, JobExecution]]

`sync(job_id: str, execution_id: str, *, client: blaxel.core.client.client.Client) ‑> Any | blaxel.core.client.models.job_execution.JobExecution | None`
:   Get job execution
    
     Returns an execution for a job by name.
    
    Args:
        job_id (str):
        execution_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, JobExecution]

`sync_detailed(job_id: str, execution_id: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.job_execution.JobExecution]`
:   Get job execution
    
     Returns an execution for a job by name.
    
    Args:
        job_id (str):
        execution_id (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, JobExecution]]