Module blaxel.api.default.get_template_file_contents
====================================================

Functions
---------

`asyncio(template_name: str, file_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> str | None`
:   Args:
        template_name (str):
        file_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        str

`asyncio_detailed(template_name: str, file_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[str]`
:   Args:
        template_name (str):
        file_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[str]

`sync(template_name: str, file_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> str | None`
:   Args:
        template_name (str):
        file_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        str

`sync_detailed(template_name: str, file_name: str, *, client: blaxel.client.AuthenticatedClient | blaxel.client.Client) ‑> blaxel.types.Response[str]`
:   Args:
        template_name (str):
        file_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[str]