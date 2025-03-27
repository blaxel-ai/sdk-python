"""
This module provides classes for handling device-based authentication,
including device login processes and bearer token management. It facilitates token refreshing
and authentication flows using device codes and bearer tokens.
"""

import base64
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Generator, Optional

from httpx import Request, Response, post

from .types import BlaxelAuth, CredentialsType


@dataclass
class DeviceLogin:
    """
    A dataclass representing a device login request.

    Attributes:
        client_id (str): The client ID for the device.
        scope (str): The scope of the authentication.
    """
    client_id: str
    scope: str


@dataclass
class DeviceLoginResponse:
    """
    A dataclass representing the response from a device login request.

    Attributes:
        client_id (str): The client ID associated with the device login.
        device_code (str): The device code for authentication.
        user_code (str): The user code for completing authentication.
        expires_in (int): Time in seconds until the device code expires.
        interval (int): Polling interval in seconds.
        verification_uri (str): URI for user to verify device login.
        verification_uri_complete (str): Complete URI including the user code for verification.
    """
    client_id: str
    device_code: str
    user_code: str
    expires_in: int
    interval: int
    verification_uri: str
    verification_uri_complete: str


@dataclass
class DeviceLoginFinalizeRequest:
    """
    A dataclass representing a device login finalize request.

    Attributes:
        grant_type (str): The type of grant being requested.
        client_id (str): The client ID for finalizing the device login.
        device_code (str): The device code to finalize login.
    """
    grant_type: str
    client_id: str
    device_code: str


@dataclass
class DeviceLoginFinalizeResponse:
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str


class DeviceMode(BlaxelAuth):
    """
    DeviceMode auth that authenticates requests using a device code.
    """
    def get_headers(self) -> Dict[str, str]:
        """
        Retrieves the authentication headers containing the Bearer token and workspace information.

        Returns:
            Dict[str, str]: A dictionary of headers with Bearer token and workspace.

        Raises:
            Exception: If token refresh fails.
        """
        err = self.refresh_if_needed()
        if err:
            raise err
        return {
            "X-Blaxel-Authorization": f"Bearer {self.credentials.access_token}",
            "X-Blaxel-Workspace": self.workspace_name,
        }

    def refresh_if_needed(self) -> Optional[Exception]:
        """
        Checks if the Bearer token needs to be refreshed and performs the refresh if necessary.

        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.
        """
        # Need to refresh token if expires in less than 10 minutes
        parts = self.credentials.access_token.split(".")
        if len(parts) != 3:
            return Exception("Invalid JWT token format")

        try:
            claims_bytes = base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4))
            claims = json.loads(claims_bytes)
        except Exception as e:
            return Exception(f"Failed to decode/parse JWT claims: {str(e)}")
        exp_time = datetime.fromtimestamp(claims["exp"])
        current_time = datetime.now()
        # Refresh if token expires in less than 10 minutes
        if current_time + timedelta(minutes=10) > exp_time:
            return self.do_refresh()

        return None

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """
        Processes the authentication flow by ensuring the Bearer token is valid and adding necessary headers.

        Parameters:
            request (Request): The HTTP request to authenticate.

        Yields:
            Request: The authenticated request.

        Raises:
            Exception: If token refresh fails.
        """
        err = self.refresh_if_needed()
        if err:
            return err

        request.headers["X-Blaxel-Authorization"] = f"Bearer {self.credentials.access_token}"
        request.headers["X-Blaxel-Workspace"] = self.workspace_name
        yield request

    def do_refresh(self) -> Optional[Exception]:
        """
        Performs the token refresh using the refresh token.

        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.
        """
        if not self.credentials.refresh_token:
            return Exception("No refresh token to refresh")

        url = f"{self.base_url}/oauth/token"
        refresh_data = {
            "grant_type": "refresh_token",
            "refresh_token": self.credentials.refresh_token,
            "device_code": self.credentials.device_code,
            "client_id": "blaxel",
        }

        try:
            response = post(url, json=refresh_data, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            finalize_response = DeviceLoginFinalizeResponse(**response.json())

            if not finalize_response.refresh_token:
                finalize_response.refresh_token = self.credentials.refresh_token

            creds = CredentialsType(
                access_token=finalize_response.access_token,
                refresh_token=finalize_response.refresh_token,
                expires_in=finalize_response.expires_in,
                device_code=self.credentials.device_code,
            )

            self.credentials = creds
            return None

        except Exception as e:
            return Exception(f"Failed to refresh token: {str(e)}")

    @property
    def token(self):
        return self.credentials.access_token
