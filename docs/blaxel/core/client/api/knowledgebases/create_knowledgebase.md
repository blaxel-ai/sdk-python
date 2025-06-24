Module blaxel.core.client.api.knowledgebases.create_knowledgebase
=================================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.models.knowledgebase.Knowledgebase | None`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.knowledgebase.Knowledgebase]`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.models.knowledgebase.Knowledgebase | None`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.knowledgebase.Knowledgebase]`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]