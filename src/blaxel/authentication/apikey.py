"""
This module provides the ApiKey class, which handles API key-based authentication for Blaxel.
"""

from typing import Generator

from httpx import Request, Response

from .types import BlaxelAuth, CredentialsType


class ApiKey(BlaxelAuth):
    """
    ApiKey auth that authenticates requests using an API key.
    """

    def __init__(self, credentials: CredentialsType, workspace_name: str, base_url: str):
        """
        Initializes the ApiKey with the given credentials and workspace name.

        Parameters:
            credentials: Credentials containing the API key.
            workspace_name (str): The name of the workspace.
            base_url (str): The base URL for authentication.
        """
        self.credentials = credentials
        self.workspace_name = workspace_name
        self.base_url = base_url

    def get_headers(self):
        """
        Retrieves the authentication headers containing the API key and workspace information.

        Returns:
            dict: A dictionary of headers with API key and workspace.
        """
        return {
            "X-Blaxel-Api-Key": self.credentials.api_key,
            "X-Blaxel-Workspace": self.workspace_name,
        }

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """
        Authenticates the request by adding API key and workspace headers.

        Parameters:
            request (Request): The HTTP request to authenticate.

        Yields:
            Request: The authenticated request.
        """
        request.headers["X-Blaxel-Api-Key"] = self.credentials.apiKey
        request.headers["X-Blaxel-Workspace"] = self.workspace_name
        yield request
