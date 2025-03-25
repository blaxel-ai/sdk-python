Module blaxel.api.templates.list_templates
==========================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.template.Template | None`
:   List templates
    
     Returns a list of all templates.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Template

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.template.Template]`
:   List templates
    
     Returns a list of all templates.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Template]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.template.Template | None`
:   List templates
    
     Returns a list of all templates.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Template

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.template.Template]`
:   List templates
    
     Returns a list of all templates.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Template]