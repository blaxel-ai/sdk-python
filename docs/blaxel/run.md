Module blaxel.run
=================
This module provides functionality for executing HTTP requests against Blaxel resources.

Classes
-------

`RunClient(client: blaxel.client.AuthenticatedClient)`
:   Provides functionality for executing HTTP requests against Blaxel resources.
    
    This module contains the RunClient class which handles authenticated HTTP requests to Blaxel
    resources. It allows users to interact with different resource types (like functions or services), supporting various HTTP methods and request parameters.
    
    Example:
        ```python
        client = new_client()
        run_client = RunClient(client)
        response = run_client.run(
            resource_type="function",
            resource_name="my-function",
            method="POST",
            json={"key": "value"}
        )
        ```
    
    Args:
        client (AuthenticatedClient): An authenticated client instance for making HTTP requests.

    ### Methods

    `run(self, resource_type: str, resource_name: str, method: str, path: str = '', headers: dict[str, str] | None = None, json: dict[str, typing.Any] | None = None, data: str | None = None, params: dict[str, str] | None = None, cloud: bool = False, service_name: str | None = None) ‑> requests.models.Response`
    :   Execute an HTTP request against a Blaxel resource.
        
        Args:
            resource_type (str): The type of resource to interact with (e.g., 'function', 'service').
            resource_name (str): The name of the specific resource.
            method (str): The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            path (str, optional): Additional path segments to append to the resource URL. Defaults to "".
            headers (dict[str, str] | None, optional): HTTP headers to include in the request. Defaults to None.
            json (dict[str, Any] | None, optional): JSON payload to send with the request. Defaults to None.
            data (str | None, optional): Raw data to send with the request. Defaults to None.
            params (dict[str, str] | None, optional): Query parameters to include in the URL. Defaults to None.
            cloud (bool, optional): Whether to use the cloud endpoint. Defaults to False.
            service_name (str | None, optional): The name of the service to use. Defaults to None.
        
        Returns:
            requests.Response: The HTTP response from the server.
        
        Raises:
            HTTPError: If the server responds with a status code >= 400.