Module blaxel.api.locations.list_locations
==========================================

Functions
---------

`asyncio(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.location_response.LocationResponse] | None`
:   List locations
    
     Returns a list of all locations available with status.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['LocationResponse']

`asyncio_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.location_response.LocationResponse]]`
:   List locations
    
     Returns a list of all locations available with status.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['LocationResponse']]

`sync(*, client: blaxel.client.AuthenticatedClient) ‑> list[blaxel.models.location_response.LocationResponse] | None`
:   List locations
    
     Returns a list of all locations available with status.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        list['LocationResponse']

`sync_detailed(*, client: blaxel.client.AuthenticatedClient) ‑> blaxel.types.Response[list[blaxel.models.location_response.LocationResponse]]`
:   List locations
    
     Returns a list of all locations available with status.
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[list['LocationResponse']]