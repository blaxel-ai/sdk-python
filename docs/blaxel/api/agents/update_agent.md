Module blaxel.api.agents.update_agent
=====================================

Functions
---------

`asyncio(agent_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.agent.Agent) ‑> blaxel.models.agent.Agent | None`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`asyncio_detailed(agent_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.agent.Agent) ‑> blaxel.types.Response[blaxel.models.agent.Agent]`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]

`sync(agent_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.agent.Agent) ‑> blaxel.models.agent.Agent | None`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`sync_detailed(agent_name: str, *, client: blaxel.client.AuthenticatedClient, body: blaxel.models.agent.Agent) ‑> blaxel.types.Response[blaxel.models.agent.Agent]`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]