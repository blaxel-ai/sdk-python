Module blaxel.api.agents.list_agent_revisions
=============================================

Functions
---------

`asyncio(agent_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.revision_metadata.RevisionMetadata] | None`
:   List all agent revisions
    
    Args:
        agent_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`asyncio_detailed(agent_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.revision_metadata.RevisionMetadata]]`
:   List all agent revisions
    
    Args:
        agent_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]

`sync(agent_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.revision_metadata.RevisionMetadata] | None`
:   List all agent revisions
    
    Args:
        agent_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['RevisionMetadata']

`sync_detailed(agent_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.revision_metadata.RevisionMetadata]]`
:   List all agent revisions
    
    Args:
        agent_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['RevisionMetadata']]