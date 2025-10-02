Module blaxel.core.client.api.jobs.list_job_executions
======================================================

Functions
---------

`asyncio(job_id: str, *, client: blaxel.core.client.client.Client, limit: blaxel.core.client.types.Unset | int = 20, offset: blaxel.core.client.types.Unset | int = 0) ‑> Any | list[blaxel.core.client.models.job_execution.JobExecution] | None`
:   List job executions
    
     Returns a list of all executions for a job by name.
    
    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['JobExecution']]

`asyncio_detailed(job_id: str, *, client: blaxel.core.client.client.Client, limit: blaxel.core.client.types.Unset | int = 20, offset: blaxel.core.client.types.Unset | int = 0) ‑> blaxel.core.client.types.Response[Any | list[blaxel.core.client.models.job_execution.JobExecution]]`
:   List job executions
    
     Returns a list of all executions for a job by name.
    
    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['JobExecution']]]

`sync(job_id: str, *, client: blaxel.core.client.client.Client, limit: blaxel.core.client.types.Unset | int = 20, offset: blaxel.core.client.types.Unset | int = 0) ‑> Any | list[blaxel.core.client.models.job_execution.JobExecution] | None`
:   List job executions
    
     Returns a list of all executions for a job by name.
    
    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[Any, list['JobExecution']]

`sync_detailed(job_id: str, *, client: blaxel.core.client.client.Client, limit: blaxel.core.client.types.Unset | int = 20, offset: blaxel.core.client.types.Unset | int = 0) ‑> blaxel.core.client.types.Response[Any | list[blaxel.core.client.models.job_execution.JobExecution]]`
:   List job executions
    
     Returns a list of all executions for a job by name.
    
    Args:
        job_id (str):
        limit (Union[Unset, int]):  Default: 20.
        offset (Union[Unset, int]):  Default: 0.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[Any, list['JobExecution']]]