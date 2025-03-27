"""
This module provides the ApiKey class, which handles API key-based authentication for Blaxel.
"""

from typing import Generator

from httpx import Request, Response

from .types import BlaxelAuth


class ApiKey(BlaxelAuth):
    """
    ApiKey auth that authenticates requests using an API key.
    """
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
        request.headers["X-Blaxel-Api-Key"] = self.credentials.api_key
        request.headers["X-Blaxel-Workspace"] = self.workspace_name
        yield request

    @property
    def token(self):
        return self.credentials.api_key
