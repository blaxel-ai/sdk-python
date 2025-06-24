Module blaxel.core.sandbox.client.api.network.post_network_process_pid_monitor
==============================================================================

Functions
---------

`asyncio(pid: int, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.port_monitor_request.PortMonitorRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.post_network_process_pid_monitor_response_200.PostNetworkProcessPidMonitorResponse200 | None`
:   Start monitoring ports for a process
    
     Start monitoring for new ports opened by a process
    
    Args:
        pid (int):
        body (PortMonitorRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]

`asyncio_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.port_monitor_request.PortMonitorRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.post_network_process_pid_monitor_response_200.PostNetworkProcessPidMonitorResponse200]`
:   Start monitoring ports for a process
    
     Start monitoring for new ports opened by a process
    
    Args:
        pid (int):
        body (PortMonitorRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]

`sync(pid: int, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.port_monitor_request.PortMonitorRequest) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.post_network_process_pid_monitor_response_200.PostNetworkProcessPidMonitorResponse200 | None`
:   Start monitoring ports for a process
    
     Start monitoring for new ports opened by a process
    
    Args:
        pid (int):
        body (PortMonitorRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]

`sync_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client, body: blaxel.core.sandbox.client.models.port_monitor_request.PortMonitorRequest) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.post_network_process_pid_monitor_response_200.PostNetworkProcessPidMonitorResponse200]`
:   Start monitoring ports for a process
    
     Start monitoring for new ports opened by a process
    
    Args:
        pid (int):
        body (PortMonitorRequest):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, PostNetworkProcessPidMonitorResponse200]]