Module blaxel.core.client.api.agents.create_agent
=================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.models.agent.Agent | None`
:   Create agent by name
    
    Args:
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.agent.Agent]`
:   Create agent by name
    
    Args:
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.models.agent.Agent | None`
:   Create agent by name
    
    Args:
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Agent

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.agent.Agent) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.agent.Agent]`
:   Create agent by name
    
    Args:
        body (Agent): Agent
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Agent]