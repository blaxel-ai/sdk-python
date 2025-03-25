"""Cache module for storing and retrieving resources."""

import os
from typing import Any, Dict, Optional

import yaml

# Global cache to store resources
_cache: Dict[str, Any] = {}


def _load_cache() -> None:
    """
    Load cache data from .cache.yaml file if it exists.
    """
    try:
        if os.path.exists('.cache.yaml'):
            with open('.cache.yaml', encoding='utf-8') as file:
                cache_string = file.read()
                cache_data = yaml.safe_load_all(cache_string)

                for doc in cache_data:
                    if doc and isinstance(doc, dict) and 'kind' in doc and 'metadata' in doc and 'name' in doc['metadata']:
                        cache_key = f"{doc['kind']}/{doc['metadata']['name']}"
                        _cache[cache_key] = doc
    except Exception:
        # Silently fail if cache file doesn't exist or is invalid
        pass

# Initialize cache on module import
_load_cache()


async def find_from_cache(resource: str, name: str) -> Optional[Any]:
    """
    Find a resource from the cache by resource type and name.

    Args:
        resource: The resource type
        name: The resource name

    Returns:
        The cached resource or None if not found
    """
    cache_key = f"{resource}/{name}"
    return _cache.get(cache_key)
