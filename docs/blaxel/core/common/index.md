Module blaxel.core.common
=========================

Sub-modules
-----------
* blaxel.core.common.env
* blaxel.core.common.internal
* blaxel.core.common.logger
* blaxel.core.common.settings

Functions
---------

`autoload() ‑> None`
:   

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

Classes
-------

`Settings()`
:   

    ### Class variables

    `auth: blaxel.core.authentication.types.BlaxelAuth`
    :

    ### Instance variables

    `base_url: str`
    :   Get the base URL for the API.

    `bl_cloud: bool`
    :   Is running on bl cloud.

    `enable_opentelemetry: bool`
    :   Get the enable opentelemetry.

    `env: str`
    :   Get the environment.

    `generation: str`
    :   Get the generation.

    `headers: Dict[str, str]`
    :   Get the headers for API requests.

    `log_level: str`
    :   Get the log level.

    `name: str`
    :   Get the name.

    `run_internal_hostname: str`
    :   Get the run internal hostname.

    `run_internal_protocol: str`
    :   Get the run internal protocol.

    `run_url: str`
    :   Get the run URL.

    `type: str`
    :   Get the type.

    `workspace: str`
    :   Get the workspace.