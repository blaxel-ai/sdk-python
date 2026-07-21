"""Contains types for authentication credentials"""

from typing import Dict

from httpx import Auth
from pydantic import BaseModel, Field


class CredentialsError(Exception):
    """Raised when Blaxel credentials are missing or incomplete.

    Surfaced eagerly with an actionable message (which env var / login step is
    missing) instead of letting a ``None`` value reach httpx header encoding or
    a misleading server-side error.
    """


class CredentialsType(BaseModel):
    """Represents authentication credentials for the API"""

    api_key: str | None = Field(default=None, description="The API key")
    client_credentials: str | None = Field(default=None, description="The client credentials")
    refresh_token: str | None = Field(default=None, description="The refresh token")
    access_token: str | None = Field(default=None, description="The access token")
    device_code: str | None = Field(default=None, description="The device code")
    expires_in: int | None = Field(default=None, description="The expiration time")
    workspace: str | None = Field(default=None, description="The workspace")


class BlaxelAuth(Auth):
    def __init__(self, credentials: CredentialsType, workspace_name: str, base_url: str):
        """
        Initializes the BlaxelAuth with the given credentials, workspace name, and base URL.

        Parameters:
            credentials: Credentials containing the Bearer token and refresh token.
            workspace_name (str): The name of the workspace.
            base_url (str): The base URL for authentication.
        """
        self.credentials = credentials
        self.workspace_name = workspace_name
        self.base_url = base_url

    def get_headers(self) -> Dict[str, str]:
        return {}

    def _ensure_workspace(self) -> str:
        """Return the workspace name, raising a clear error if it is missing.

        Called before emitting the ``X-Blaxel-Workspace`` header so a ``None``
        workspace never reaches httpx (which would raise an opaque
        ``'NoneType' object has no attribute 'encode'``).
        """
        if not self.workspace_name:
            raise CredentialsError(
                "Blaxel workspace is missing. Set the BL_WORKSPACE environment "
                "variable, or run `bl login`, to authenticate your requests."
            )
        return self.workspace_name

    @property
    def token(self):
        raise NotImplementedError("Subclasses must implement the token property")


class MissingCredentials(BlaxelAuth):
    """Auth placeholder used when no usable Blaxel credentials were resolved.

    Construction is side-effect free, so ``import blaxel`` succeeds without
    credentials. The actionable error is raised only when the auth object is
    actually used to build a request (headers, auth flow, or token access),
    which is what every controlplane, run, and sandbox call goes through.
    """

    def __init__(self, base_url: str = "", message: str | None = None):
        self.credentials = CredentialsType()
        self.workspace_name = None
        self.base_url = base_url
        self._message = message or (
            "No Blaxel credentials found. Set the BL_API_KEY and BL_WORKSPACE "
            "environment variables, or run `bl login`."
        )

    def _raise(self):
        raise CredentialsError(self._message)

    def get_headers(self) -> Dict[str, str]:
        self._raise()

    def auth_flow(self, request):
        self._raise()

    @property
    def token(self):
        self._raise()
