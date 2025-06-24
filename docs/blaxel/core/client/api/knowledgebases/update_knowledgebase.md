Module blaxel.core.client.api.knowledgebases.update_knowledgebase
=================================================================

Functions
---------

`asyncio(knowledgebase_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.models.knowledgebase.Knowledgebase | None`
:   Update knowledgebase
    
     Updates an knowledgebase.
    
    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`asyncio_detailed(knowledgebase_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.knowledgebase.Knowledgebase]`
:   Update knowledgebase
    
     Updates an knowledgebase.
    
    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]

`sync(knowledgebase_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.models.knowledgebase.Knowledgebase | None`
:   Update knowledgebase
    
     Updates an knowledgebase.
    
    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Knowledgebase

`sync_detailed(knowledgebase_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.knowledgebase.Knowledgebase) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.knowledgebase.Knowledgebase]`
:   Update knowledgebase
    
     Updates an knowledgebase.
    
    Args:
        knowledgebase_name (str):
        body (Knowledgebase): Knowledgebase
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Knowledgebase]