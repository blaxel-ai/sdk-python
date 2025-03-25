Module blaxel.deploy.format
===========================
This module provides utility functions to format deployment configurations into YAML-compatible strings.
It includes functions to convert arguments, parameters, dictionaries, and agent chains into properly formatted JSON or YAML strings.

Functions
---------

`arg_to_dict(arg: ast.keyword)`
:   Converts an AST keyword argument to a dictionary.
    
    Args:
        arg (ast.keyword): The AST keyword argument.
    
    Returns:
        dict: The resulting dictionary.

`arg_to_list(arg: ast.List)`
:   

`format_value(v)`
:   Formats an AST node value into its Python equivalent.
    
    Args:
        v (ast.AST): The AST node to format.
    
    Returns:
        Any: The formatted Python value.