Module blaxel.core.client.api.customdomains.update_custom_domain
================================================================

Functions
---------

`asyncio(domain_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.custom_domain.CustomDomain) ‑> blaxel.core.client.models.custom_domain.CustomDomain | None`
:   Update custom domain
    
    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CustomDomain

`asyncio_detailed(domain_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.custom_domain.CustomDomain) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.custom_domain.CustomDomain]`
:   Update custom domain
    
    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CustomDomain]

`sync(domain_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.custom_domain.CustomDomain) ‑> blaxel.core.client.models.custom_domain.CustomDomain | None`
:   Update custom domain
    
    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        CustomDomain

`sync_detailed(domain_name: str, *, client: blaxel.core.client.client.Client, body: blaxel.core.client.models.custom_domain.CustomDomain) ‑> blaxel.core.client.types.Response[blaxel.core.client.models.custom_domain.CustomDomain]`
:   Update custom domain
    
    Args:
        domain_name (str):
        body (CustomDomain): Custom domain for preview deployments
            The custom domain represents a base domain (e.g., example.com) that will be used
            to serve preview deployments. Each preview will be accessible at a subdomain:
            <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)
    
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
    
    Returns:
        Response[CustomDomain]