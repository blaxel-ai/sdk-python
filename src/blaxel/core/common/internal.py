import hashlib
from logging import getLogger
from typing import Optional

from .env import env

logger = getLogger(__name__)


def get_alphanumeric_limited_hash(input_str, max_size=48):
    """
    Create an alphanumeric hash using MD5 that can be reproduced in Go, TypeScript, and Python.

    Args:
        input_str (str): The input string to hash
        max_size (int): The maximum length of the returned hash

    Returns:
        str: An alphanumeric hash of the input string, limited to max_size
    """
    # Calculate MD5 hash and convert to hexadecimal
    hash_hex = hashlib.md5(input_str.encode("utf-8")).hexdigest()

    # Limit to max_size
    if len(hash_hex) > max_size:
        return hash_hex[:max_size]

    return hash_hex


def get_global_unique_hash(workspace: str, type: str, name: str) -> str:
    """
    Generate a unique hash for a combination of workspace, type, and name.

    Args:
        workspace: The workspace identifier
        type: The type identifier
        name: The name identifier

    Returns:
        A unique alphanumeric hash string of maximum length 48
    """
    global_unique_name = f"{workspace}-{type}-{name}"
    hash = get_alphanumeric_limited_hash(global_unique_name, 48)
    return hash


def pluralize(type_str: str) -> str:
    """
    Convert a string to its plural form following English pluralization rules.

    Args:
        type_str: The input string to pluralize

    Returns:
        The pluralized form of the input string
    """
    word = type_str.lower()

    # Words ending in s, ss, sh, ch, x, z - add 'es'
    if (
        word.endswith("s")
        or word.endswith("ss")
        or word.endswith("sh")
        or word.endswith("ch")
        or word.endswith("x")
        or word.endswith("z")
    ):
        return type_str + "es"

    # Words ending in consonant + y - change y to ies
    if word.endswith("y") and len(word) > 1:
        before_y = word[-2]
        if before_y not in "aeiou":
            return type_str[:-1] + "ies"

    # Words ending in f or fe - change to ves
    if word.endswith("f"):
        return type_str[:-1] + "ves"
    if word.endswith("fe"):
        return type_str[:-2] + "ves"

    # Words ending in consonant + o - add 'es'
    if word.endswith("o") and len(word) > 1:
        before_o = word[-2]
        if before_o not in "aeiou":
            return type_str + "es"

    # Default case - just add 's'
    return type_str + "s"


def get_forced_url(type_str: str, name: str) -> Optional[str]:
    """
    Check for forced URLs in environment variables using both plural and singular forms.

    Args:
        type_str: The type identifier
        name: The name identifier

    Returns:
        The forced URL if found in environment variables, None otherwise
    """
    plural_type = pluralize(type_str)
    env_var = name.replace("-", "_").upper()

    # BL_FUNCTIONS_NAME_URL (plural form)
    plural_env_key = f"BL_{plural_type.upper()}_{env_var}_URL"
    if env[plural_env_key] is not None:
        return env[plural_env_key]

    # BL_FUNCTION_NAME_URL (singular form)
    singular_env_key = f"BL_{type_str.upper()}_{env_var}_URL"
    if env[singular_env_key] is not None:
        return env[singular_env_key]

    return None


def get_workload_type_short(type_str: str) -> str:
    """
    Get the short form of a workload type for cloud URL generation.
    
    Args:
        type_str: The full type name (e.g., 'agent', 'mcp', 'function', 'sandbox', etc.)
    
    Returns:
        The short form of the type (e.g., 'agt', 'mcp', 'sbx', 'job', 'mdl')
    """
    lower_type = type_str.lower()
    
    # Map type names to their short forms
    type_mapping = {
        'agent': 'agt',
        'agents': 'agt',
        'mcp': 'mcp',
        'mcps': 'mcp',
        'function': 'mcp',
        'functions': 'mcp',
        'sandbox': 'sbx',
        'sandboxes': 'sbx',
        'job': 'job',
        'jobs': 'job',
        'model': 'mdl',
        'models': 'mdl',
    }
    
    # Return mapped value or first 3 letters as fallback
    return type_mapping.get(lower_type, lower_type[:3])


def generate_internal_url(
    workspace: str,
    type_str: str,
    name: str,
    env: str,
    protocol: str,
    hostname: str,
    bl_cloud: bool,
    workspace_id: str
) -> str:
    """
    Generate an internal URL based on cloud or legacy format.
    
    Args:
        workspace: The workspace name
        type_str: The workload type (e.g., 'agent', 'mcp', 'sandbox', 'job')
        name: The workload name
        env: The environment (e.g., 'dev', 'prod')
        protocol: The protocol to use (e.g., 'https')
        hostname: The internal hostname
        bl_cloud: Whether cloud mode is enabled
        workspace_id: The workspace ID for cloud mode
    
    Returns:
        The formatted internal URL
    """
    if bl_cloud and workspace_id:
        # New cloud format: bl-ENV-WORKLOAD_CALLED_NAME-WORKLOAD_TYPE_SHORT-WORKSPACE_ID
        workload_type_short = get_workload_type_short(type_str)
        subdomain = f"bl-{env}-{name}-{workload_type_short}-{workspace_id}"
        return f"{protocol}://{subdomain}.{hostname}"
    else:
        # Legacy format: bl-ENV-HASH.internalhostname
        hash_value = get_global_unique_hash(workspace, type_str, name)
        return f"{protocol}://bl-{env}-{hash_value}.{hostname}"
