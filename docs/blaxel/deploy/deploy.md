Module blaxel.deploy.deploy
===========================
This module provides functionalities to generate and manage Blaxel deployment configurations.
It includes functions to set default deployment values, create deployment configurations from resources,
format deployments, and clean up auto-generated deployments.

Functions
---------

`clean_auto_generated(directory: str, type: Literal['agent', 'function'], deployments: list[tuple[blaxel.deploy.parser.Resource, blaxel.models.agent.Agent | blaxel.models.function.Function]])`
:   Cleans up auto-generated deployments of a specific type.
    
    Args:
        directory (str): Base directory containing deployments.
        type (Literal["agent", "function"]): Type of deployment to clean ("agent" or "function").
        deployments (list[tuple[Resource, Agent | Function]]): List of deployment resources and configurations.

`dockerfile(type: Literal['agent', 'function'], resource: blaxel.deploy.parser.Resource, deployment: blaxel.models.agent.Agent | blaxel.models.function.Function) ‑> str`
:   Generates Dockerfile content for agent or function deployment.
    
    Args:
        type (Literal["agent", "function"]): Type of deployment
        resource (Resource): Resource to be deployed
        deployment (Agent | Function): Resource configuration
    
    Returns:
        str: Dockerfile content

`generate_blaxel_deployment(directory: str, name: str)`
:   Generates all necessary deployment files for Blaxel agents and functions.
    
    Args:
        directory (str): Target directory for generated files.
        name (str): Name identifier for the deployment.
    
    Creates:
        - Agent and function YAML configurations.
        - Dockerfiles for each deployment.
        - Directory structure for agents and functions.

`get_agent_yaml(agent: blaxel.models.agent.Agent, functions: list[tuple[blaxel.deploy.parser.Resource, blaxel.models.function.Function]], settings: blaxel.common.settings.Settings, client: blaxel.client.AuthenticatedClient) ‑> str`
:   Generates YAML configuration for an agent deployment.
    
    Args:
        agent (Agent): Agent deployment configuration
        functions (list[tuple[Resource, FunctionDeployment]]): List of associated functions
        settings (Settings): Application settings
    
    Returns:
        str: YAML configuration string

`get_blaxel_deployment_from_resource(settings: blaxel.common.settings.Settings, resource: blaxel.deploy.parser.Resource) ‑> blaxel.models.agent.Agent | blaxel.models.function.Function | blaxel.models.function_kit.FunctionKit`
:   Creates a deployment configuration from a given resource.
    
    Args:
        resource (Resource): The resource to create a deployment for.
    
    Returns:
        Agent | Function: The deployment configuration.

`get_flavors(flavors: list[blaxel.models.flavor.Flavor]) ‑> str`
:   Converts a list of Flavor objects to a JSON string.
    
    Args:
        flavors (list[Flavor]): List of Flavor objects.
    
    Returns:
        str: JSON string representation of flavors.

`get_function_yaml(function: blaxel.models.function.Function, settings: blaxel.common.settings.Settings, client: blaxel.client.AuthenticatedClient) ‑> str`
:   Generates YAML configuration for a function deployment.
    
    Args:
        function (FunctionDeployment): Function deployment configuration
        settings (Settings): Application settings
    
    Returns:
        str: YAML configuration string

`handle_function_kit(deployment: blaxel.models.function.Function)`
:   Handles the function kit for a deployment.

`set_default_values(resource: blaxel.deploy.parser.Resource, deployment: blaxel.models.agent.Agent | blaxel.models.function.Function)`
:   Sets default values for a deployment based on the resource and deployment type.
    
    Parameters:
        resource (Resource): The resource information.
        deployment (Agent | Function): The deployment instance to set defaults for.
    
    Returns:
        Agent | Function: The updated deployment with default values set.