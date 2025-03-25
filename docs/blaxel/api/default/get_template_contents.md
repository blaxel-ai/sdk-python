Module blaxel.api.default.get_template_contents
===============================================

Functions
---------

`asyncio(template_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> list[str] | None`
:   Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list[str]

`asyncio_detailed(template_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[list[str]]`
:   Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list[str]]

`sync(template_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> list[str] | None`
:   Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list[str]

`sync_detailed(template_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[list[str]]`
:   Args:
        template_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list[str]]