Module blaxel.core.client.api.models.create_model
=================================================

Functions
---------

`asyncio(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.models.model.Model | None`
:   Create model
    
     Creates a model.
    
    Args:
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`asyncio_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Create model
    
     Creates a model.
    
    Args:
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]

`sync(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.models.model.Model | None`
:   Create model
    
     Creates a model.
    
    Args:
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`sync_detailed(*, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Create model
    
     Creates a model.
    
    Args:
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]