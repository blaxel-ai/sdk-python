Module blaxel.core.client.api.default.get_template
==================================================

Functions
---------

`asyncio(template_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.template.Template | None`
:   Get template
    
     Returns a template by name.
    
    Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Template

`asyncio_detailed(template_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.template.Template]`
:   Get template
    
     Returns a template by name.
    
    Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Template]

`sync(template_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.models.template.Template | None`
:   Get template
    
     Returns a template by name.
    
    Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Template

`sync_detailed(template_name: str, *, client: blaxel.core.client.client.Client) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.template.Template]`
:   Get template
    
     Returns a template by name.
    
    Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Template]