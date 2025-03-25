Module blaxel.deploy.parser
===========================
This module provides classes and functions for parsing deployment resources within Blaxel.
It includes the Resource dataclass for representing deployment resources and functions to extract and process resources
decorated within Python files.

Functions
---------

`get_description(description: str | None, resource: blaxel.deploy.parser.Resource) ‑> str`
:   Gets the description of a function from either a provided description or the function's docstring.
    
    Args:
        description (str | None): Optional explicit description
        resource (Resource): The resource object containing the function
    
    Returns:
        str: The function description

`get_resources(from_decorator, dir) ‑> list[blaxel.deploy.parser.Resource]`
:   Scans through Python files in a directory to find functions decorated with a specific decorator.
    
    Args:
        from_decorator (str): The name of the decorator to search for
        dir (str): The directory to scan, defaults to "src"
    
    Returns:
        list[Resource]: List of Resource objects containing information about decorated functions

`get_schema(resource: blaxel.deploy.parser.Resource) ‑> blaxel.models.function_schema.FunctionSchema`
:   Extracts parameter information from a function's signature and docstring.
    
    Args:
        resource (Resource): The resource object containing the function to analyze
    
    Returns:
        FunctionSchema: OpenAPI schema for the function parameters

Classes
-------

`Resource(type: Literal['agent', 'function', 'kit'], module: Callable, name: str, decorator: ast.Call, func: Callable)`
:   A dataclass representing a deployment resource.
    
    Attributes:
        type (Literal["agent", "function"]): The type of deployment ("agent" or "function").
        module (Callable): The module containing the deployment.
        name (str): The name of the deployment.
        decorator (ast.Call): The decorator AST node used on the deployment function.
        func (Callable): The deployment function.

    ### Instance variables

    `decorator: ast.Call`
    :

    `func: Callable`
    :

    `module: Callable`
    :

    `name: str`
    :

    `type: Literal['agent', 'function', 'kit']`
    :