Module blaxel.core.client.api.models.update_model
=================================================

Functions
---------

`asyncio(model_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.models.model.Model | None`
:   Create or update model
    
     Update a model by name.
    
    Args:
        model_name (str):
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`asyncio_detailed(model_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Create or update model
    
     Update a model by name.
    
    Args:
        model_name (str):
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]

`sync(model_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.models.model.Model | None`
:   Create or update model
    
     Update a model by name.
    
    Args:
        model_name (str):
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`sync_detailed(model_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.model.Model) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.model.Model]`
:   Create or update model
    
     Update a model by name.
    
    Args:
        model_name (str):
        body (Model): Logical object representing a model
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]