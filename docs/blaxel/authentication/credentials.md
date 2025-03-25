Module blaxel.authentication.credentials
========================================
This module provides classes and functions for managing credentials and workspace configurations.
It includes functionalities to load, save, and manage authentication credentials, as well as to handle
workspace contexts and configurations.

Functions
---------

`clear_credentials(workspace_name: str)`
:   Clears the credentials for the specified workspace.
    
    Parameters:
        workspace_name (str): The name of the workspace whose credentials are to be cleared.

`create_home_dir_if_missing()`
:   Creates the Blaxel home directory if it does not exist.
    
    Logs a warning if credentials already exist or an error if directory creation fails.

`current_context() ‑> blaxel.authentication.credentials.ContextConfig`
:   Retrieves the current context configuration.
    
    Returns:
        ContextConfig: The current context configuration.

`list_workspaces() ‑> List[str]`
:   Lists all available workspace names from the configuration.
    
    Returns:
        List[str]: A list of workspace names.

`load_config() ‑> blaxel.authentication.credentials.Config`
:   Loads the configuration from the user's home directory.
    
    Returns:
        Config: The loaded configuration.

`load_credentials(workspace_name: str) ‑> blaxel.authentication.credentials.Credentials`
:   Loads credentials for the specified workspace.
    
    Parameters:
        workspace_name (str): The name of the workspace whose credentials are to be loaded.
    
    Returns:
        Credentials: The credentials associated with the workspace. Returns empty credentials if not found.

`load_credentials_from_settings(settings: blaxel.common.settings.Settings) ‑> blaxel.authentication.credentials.Credentials`
:   Loads credentials from the provided settings.
    
    Parameters:
        settings (Settings): The settings containing authentication information.
    
    Returns:
        Credentials: The loaded credentials from settings.

`save_config(config: blaxel.authentication.credentials.Config)`
:   Saves the provided configuration to the user's home directory.
    
    Parameters:
        config (Config): The configuration to save.
    
    Raises:
        RuntimeError: If the home directory cannot be determined.

`save_credentials(workspace_name: str, credentials: blaxel.authentication.credentials.Credentials)`
:   Saves the provided credentials for the specified workspace.
    
    Parameters:
        workspace_name (str): The name of the workspace.
        credentials (Credentials): The credentials to save.

`set_current_workspace(workspace_name: str)`
:   Sets the current workspace in the configuration.
    
    Parameters:
        workspace_name (str): The name of the workspace to set as current.

Classes
-------

`Config(workspaces: List[blaxel.authentication.credentials.WorkspaceConfig] = None, context: blaxel.authentication.credentials.ContextConfig = None)`
:   A dataclass representing the overall configuration, including workspaces and context.
    
    Attributes:
        workspaces (List[WorkspaceConfig]): A list of workspace configurations.
        context (ContextConfig): The current context configuration.

    ### Instance variables

    `context: blaxel.authentication.credentials.ContextConfig`
    :

    `workspaces: List[blaxel.authentication.credentials.WorkspaceConfig]`
    :

    ### Methods

    `to_json(self) ‑> dict`
    :   Converts the Config dataclass to a JSON-compatible dictionary.
        
        Returns:
            dict: The JSON representation of the configuration.

`ContextConfig(workspace: str = '')`
:   A dataclass representing the current context configuration.
    
    Attributes:
        workspace (str): The name of the current workspace.

    ### Instance variables

    `workspace: str`
    :

`Credentials(apiKey: str = '', access_token: str = '', refresh_token: str = '', expires_in: int = 0, device_code: str = '', client_credentials: str = '')`
:   A dataclass representing user credentials for authentication.
    
    Attributes:
        apiKey (str): The API key.
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        expires_in (int): Token expiration time in seconds.
        device_code (str): The device code for device authentication.
        client_credentials (str): The client credentials for authentication.

    ### Instance variables

    `access_token: str`
    :

    `apiKey: str`
    :

    `client_credentials: str`
    :

    `device_code: str`
    :

    `expires_in: int`
    :

    `refresh_token: str`
    :

`WorkspaceConfig(name: str, credentials: blaxel.authentication.credentials.Credentials)`
:   A dataclass representing the configuration for a workspace.
    
    Attributes:
        name (str): The name of the workspace.
        credentials (Credentials): The credentials associated with the workspace.

    ### Instance variables

    `credentials: blaxel.authentication.credentials.Credentials`
    :

    `name: str`
    :