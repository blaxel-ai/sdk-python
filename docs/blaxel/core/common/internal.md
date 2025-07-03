Module blaxel.core.common.internal
==================================

Functions
---------

`get_alphanumeric_limited_hash(input_str, max_size=48)`
:   Create an alphanumeric hash using MD5 that can be reproduced in Go, TypeScript, and Python.
    
    Args:
        input_str (str): The input string to hash
        max_size (int): The maximum length of the returned hash
    
    Returns:
        str: An alphanumeric hash of the input string, limited to max_size

`get_forced_url(type_str: str, name: str) ‑> str | None`
:   Check for forced URLs in environment variables using both plural and singular forms.
    
    Args:
        type_str: The type identifier
        name: The name identifier
    
    Returns:
        The forced URL if found in environment variables, None otherwise

`get_global_unique_hash(workspace: str, type: str, name: str) ‑> str`
:   Generate a unique hash for a combination of workspace, type, and name.
    
    Args:
        workspace: The workspace identifier
        type: The type identifier
        name: The name identifier
    
    Returns:
        A unique alphanumeric hash string of maximum length 48

`pluralize(type_str: str) ‑> str`
:   Convert a string to its plural form following English pluralization rules.
    
    Args:
        type_str: The input string to pluralize
    
    Returns:
        The pluralized form of the input string