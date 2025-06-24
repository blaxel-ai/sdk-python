Module blaxel.core.client.api.agents.update_agent
=================================================

Functions
---------

`asyncio(agent_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.models.agent.Agent | None`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`asyncio_detailed(agent_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.agent.Agent]`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]

`sync(agent_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.models.agent.Agent | None`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`sync_detailed(agent_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.agent.Agent]`
:   Update agent by name
    
    Args:
        agent_name (str):
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]