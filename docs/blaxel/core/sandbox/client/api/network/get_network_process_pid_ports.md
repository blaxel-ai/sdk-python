Module blaxel.core.sandbox.client.api.network.get_network_process_pid_ports
===========================================================================

Functions
---------

`asyncio(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.get_network_process_pid_ports_response_200.GetNetworkProcessPidPortsResponse200 | None`
:   Get open ports for a process
    
     Get a list of all open ports for a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, GetNetworkProcessPidPortsResponse200]

`asyncio_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.get_network_process_pid_ports_response_200.GetNetworkProcessPidPortsResponse200]`
:   Get open ports for a process
    
     Get a list of all open ports for a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, GetNetworkProcessPidPortsResponse200]]

`sync(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.get_network_process_pid_ports_response_200.GetNetworkProcessPidPortsResponse200 | None`
:   Get open ports for a process
    
     Get a list of all open ports for a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Union[ErrorResponse, GetNetworkProcessPidPortsResponse200]

`sync_detailed(pid: int, *, client: blaxel.core.sandbox.client.client.Client) ‑> blaxel.core.sandbox.client.types.Response[blaxel.core.sandbox.client.models.error_response.ErrorResponse | blaxel.core.sandbox.client.models.get_network_process_pid_ports_response_200.GetNetworkProcessPidPortsResponse200]`
:   Get open ports for a process
    
     Get a list of all open ports for a process
    
    Args:
        pid (int):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Union[ErrorResponse, GetNetworkProcessPidPortsResponse200]]