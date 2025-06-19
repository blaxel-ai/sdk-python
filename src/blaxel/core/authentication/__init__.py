import os
from logging import getLogger
from pathlib import Path
from typing import Optional

import yaml

from .apikey import ApiKey
from .clientcredentials import ClientCredentials
from .devicemode import DeviceMode
from .types import BlaxelAuth, CredentialsType

logger = getLogger(__name__)

def get_credentials() -> Optional[CredentialsType]:
    """
    Get credentials from environment variables or config file.

    Returns:
        Optional[CredentialsType]: The credentials or None if not found
    """
    def get_workspace():
        if os.environ.get("BL_WORKSPACE"):
            return os.environ.get("BL_WORKSPACE")
        home_dir = Path.home()
        config_path = home_dir / '.blaxel' / 'config.yaml'
        with open(config_path, encoding='utf-8') as f:
            config_json = yaml.safe_load(f)
        return config_json.get("context", {}).get("workspace")

    if os.environ.get("BL_API_KEY"):
        return CredentialsType(
            api_key=os.environ.get("BL_API_KEY"),
            workspace=get_workspace()
        )

    if os.environ.get("BL_CLIENT_CREDENTIALS"):
        return CredentialsType(
            client_credentials=os.environ.get("BL_CLIENT_CREDENTIALS"),
            workspace=get_workspace()
        )

    try:
        home_dir = Path.home()
        config_path = home_dir / '.blaxel' / 'config.yaml'

        with open(config_path, encoding='utf-8') as f:
            config_json = yaml.safe_load(f)

        workspace_name = os.environ.get("BL_WORKSPACE") or config_json.get("context", {}).get("workspace")

        for workspace in config_json.get("workspaces", []):
            if workspace.get("name") == workspace_name:
                credentials = workspace.get("credentials", {})
                credentials["workspace"] = workspace_name
                return CredentialsType(
                    workspace=credentials["workspace"],
                    api_key=credentials.get("api_key"),
                    client_credentials=credentials.get("client_credentials"),
                    refresh_token=credentials.get("refresh_token"),
                    access_token=credentials.get("access_token"),
                    device_code=credentials.get("device_code"),
                    expires_in=credentials.get("expires_in")
                )

        return None
    except Exception:
        return None


def auth(env: str, base_url: str) -> BlaxelAuth:
    """
    Create and return the appropriate credentials object based on available credentials.

    Returns:
        Credentials: The credentials object
    """
    credentials = get_credentials()

    if not credentials:
        return None

    if credentials.api_key:
        logger.debug("Using API key for authentication")
        return ApiKey(credentials, credentials.workspace, base_url)

    if credentials.client_credentials:
        logger.debug("Using client credentials for authentication")
        return ClientCredentials(credentials, credentials.workspace, base_url)

    if credentials.device_code:
        logger.debug("Using device code for authentication")
        return DeviceMode(credentials, credentials.workspace, base_url)

    return BlaxelAuth(credentials, credentials.workspace, base_url)

__all__ = ["BlaxelAuth", "CredentialsType"]