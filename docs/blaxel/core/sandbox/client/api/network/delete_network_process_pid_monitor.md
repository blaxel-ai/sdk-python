Module blaxel.core.sandbox.client.api.network.delete_network_process_pid_monitor
================================================================================

Functions
---------

`asyncio(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.delete_network_process_pid_monitor_response_200.DeleteNetworkProcessPidMonitorResponse200 | blaxel.core.sandbox.client.models.error_response.ErrorResponse | None`
:   Stop monitoring ports for a process
    
     Stop monitoring for new ports opened by a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]

`asyncio_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.delete_network_process_pid_monitor_response_200.DeleteNetworkProcessPidMonitorResponse200 | blaxel.core.sandbox.client.models.error_response.ErrorResponse]`
:   Stop monitoring ports for a process
    
     Stop monitoring for new ports opened by a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]

`sync(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.delete_network_process_pid_monitor_response_200.DeleteNetworkProcessPidMonitorResponse200 | blaxel.core.sandbox.client.models.error_response.ErrorResponse | None`
:   Stop monitoring ports for a process
    
     Stop monitoring for new ports opened by a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]

`sync_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.delete_network_process_pid_monitor_response_200.DeleteNetworkProcessPidMonitorResponse200 | blaxel.core.sandbox.client.models.error_response.ErrorResponse]`
:   Stop monitoring ports for a process
    
     Stop monitoring for new ports opened by a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[DeleteNetworkProcessPidMonitorResponse200, ErrorResponse]]