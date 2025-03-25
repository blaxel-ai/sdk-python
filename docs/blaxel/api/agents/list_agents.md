Module blaxel.api.agents.list_agents
====================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.agent.Agent] | None`
:   List all agents
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Agent']

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.agent.Agent]]`
:   List all agents
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Agent']]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.agent.Agent] | None`
:   List all agents
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['Agent']

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.agent.Agent]]`
:   List all agents
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['Agent']]