Module blaxel.core.cache.cache
==============================
Cache module for storing and retrieving resources.

Functions
---------

`find_from_cache(resource: str, name: str) ‑> Any | None`
:   Find a resource from the cache by resource type and name.
    
    Args:
        resource: The resource type
        name: The resource name
    
    Returns:
        The cached resource or None if not found