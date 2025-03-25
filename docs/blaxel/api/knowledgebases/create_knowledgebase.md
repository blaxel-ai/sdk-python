Module blaxel.api.knowledgebases.create_knowledgebase
=====================================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.knowledgebase.Knowledgebase) ‑> blaxel.models.knowledgebase.Knowledgebase | None`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.knowledgebase.Knowledgebase) ‑> blaxel.types.Response[blaxel.models.knowledgebase.Knowledgebase]`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]

`sync(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.knowledgebase.Knowledgebase) ‑> blaxel.models.knowledgebase.Knowledgebase | None`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`sync_detailed(*, client: blaxel.client.AuthenticatedClient, body: blaxel.models.knowledgebase.Knowledgebase) ‑> blaxel.types.Response[blaxel.models.knowledgebase.Knowledgebase]`
:   Create knowledgebase
    
     Creates an knowledgebase.
    
    Args:
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]