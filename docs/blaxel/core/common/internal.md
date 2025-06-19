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

`get_global_unique_hash(workspace: str, type: str, name: str) ‑> str`
:   Generate a unique hash for a combination of workspace, type, and name.
    
    Args:
        workspace: The workspace identifier
        type: The type identifier
        name: The name identifier
    
    Returns:
        A unique alphanumeric hash string of maximum length 48