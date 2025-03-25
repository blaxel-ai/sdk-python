Module blaxel.common.secrets
============================

Classes
-------

`Secret()`
:   A utility class for managing environment secrets.
    
    Provides static methods to retrieve and set secret values, supporting both standard and
    prefixed environment variable naming conventions.

    ### Static methods

    `get(name: str)`
    :   Retrieves the value of a secret environment variable.
        
        This method first attempts to get the value using the standard name. If not found,
        it tries with a "bl_" prefix.
        
        Parameters:
            name (str): The name of the environment variable to retrieve.
        
        Returns:
            str: The value of the environment variable if found, otherwise an empty string.

    `set(name: str, value: str)`
    :   Sets the value of a secret environment variable.
        
        This method sets the value using the standard name, allowing for consistent secret management.
        
        Parameters:
            name (str): The name of the environment variable to set.
            value (str): The value to assign to the environment variable.