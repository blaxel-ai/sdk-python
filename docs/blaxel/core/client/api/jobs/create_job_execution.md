Module blaxel.core.client.api.jobs.create_job_execution
=======================================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_job_execution_request.CreateJobExecutionRequest) ‑> Any | blaxel.core.client.models.job_execution.JobExecution | None`
:   Create job execution
    
     Creates a new execution for a job by name.
    
    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, JobExecution]

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_job_execution_request.CreateJobExecutionRequest) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.job_execution.JobExecution]`
:   Create job execution
    
     Creates a new execution for a job by name.
    
    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, JobExecution]]

`sync(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_job_execution_request.CreateJobExecutionRequest) ‑> Any | blaxel.core.client.models.job_execution.JobExecution | None`
:   Create job execution
    
     Creates a new execution for a job by name.
    
    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, JobExecution]

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.create_job_execution_request.CreateJobExecutionRequest) ‑> blaxel.core.client.types.Response[Any | blaxel.core.client.models.job_execution.JobExecution]`
:   Create job execution
    
     Creates a new execution for a job by name.
    
    Args:
        job_id (str):
        body (CreateJobExecutionRequest): Request to create a job execution
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, JobExecution]]