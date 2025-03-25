"""Contains types for authentication credentials"""

from typing import Dict, Optional

from httpx import Auth
from pydantic import BaseModel, Field


class CredentialsType(BaseModel):
    """Represents authentication credentials for the API"""

    api_key: Optional[str] = Field(default=None, description="The API key")
    client_credentials: Optional[str] = Field(default=None, description="The client credentials")
    refresh_token: Optional[str] = Field(default=None, description="The refresh token")
    access_token: Optional[str] = Field(default=None, description="The access token")
    device_code: Optional[str] = Field(default=None, description="The device code")
    expires_in: Optional[int] = Field(default=None, description="The expiration time")
    workspace: Optional[str] = Field(default=None, description="The workspace")

class BlaxelAuth(Auth):
    def get_headers(self) -> Dict[str, str]:
        return {}
