Module blaxel.api.models.delete_model
=====================================

Functions
---------

`asyncio(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.model.Model | None`
:   Delete model
    
     Deletes a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`asyncio_detailed(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.model.Model]`
:   Delete model
    
     Deletes a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]

`sync(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.models.model.Model | None`
:   Delete model
    
     Deletes a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Model

`sync_detailed(model_name: str, *, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[blaxel.models.model.Model]`
:   Delete model
    
     Deletes a model by name.
    
    Args:
        model_name (str):
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[Model]