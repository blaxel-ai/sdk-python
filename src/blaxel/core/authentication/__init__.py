import os
from logging import getLogger
from pathlib import Path

import yaml

from .apikey import ApiKey
from .clientcredentials import ClientCredentials
from .devicemode import DeviceMode
from .types import BlaxelAuth, CredentialsError, CredentialsType, MissingCredentials

logger = getLogger(__name__)


def _missing_credentials_message() -> str:
    """Build an actionable message naming exactly which piece is missing."""
    has_workspace = bool(os.environ.get("BL_WORKSPACE"))
    has_api_key = bool(os.environ.get("BL_API_KEY"))
    if has_workspace and not has_api_key:
        return (
            "Blaxel API key is missing. Set the BL_API_KEY environment variable, "
            "or run `bl login`, to authenticate (BL_WORKSPACE is already set)."
        )
    if has_api_key and not has_workspace:
        return (
            "Blaxel workspace is missing. Set the BL_WORKSPACE environment variable, "
            "or run `bl login`, to authenticate (BL_API_KEY is already set)."
        )
    return (
        "No Blaxel credentials found. Set the BL_API_KEY and BL_WORKSPACE "
        "environment variables, or run `bl login`."
    )


def get_credentials() -> CredentialsType | None:
    """
    Get credentials from environment variables or config file.

    Returns:
        CredentialsType | None: The credentials or None if not found
    """

    def get_workspace():
        if os.environ.get("BL_WORKSPACE"):
            return os.environ.get("BL_WORKSPACE")
        try:
            home_dir = Path.home()
            config_path = home_dir / ".blaxel" / "config.yaml"
            with open(config_path, encoding="utf-8") as f:
                config_json = yaml.safe_load(f) or {}
            return config_json.get("context", {}).get("workspace")
        except Exception:
            # No config file (e.g. running in a fresh sandbox with only
            # BL_API_KEY set) must not crash credential resolution; the
            # missing workspace is reported clearly at request time instead.
            return None

    if os.environ.get("BL_API_KEY"):
        return CredentialsType(api_key=os.environ.get("BL_API_KEY"), workspace=get_workspace())

    if os.environ.get("BL_CLIENT_CREDENTIALS"):
        return CredentialsType(
            client_credentials=os.environ.get("BL_CLIENT_CREDENTIALS"),
            workspace=get_workspace(),
        )

    try:
        home_dir = Path.home()
        config_path = home_dir / ".blaxel" / "config.yaml"

        with open(config_path, encoding="utf-8") as f:
            config_json = yaml.safe_load(f)

        workspace_name = os.environ.get("BL_WORKSPACE") or config_json.get("context", {}).get(
            "workspace"
        )

        for workspace in config_json.get("workspaces", []):
            if workspace.get("name") == workspace_name:
                # Set BL_ENV from config.yaml workspace if not already set via env vars
                if not os.environ.get("BL_ENV") and workspace.get("env"):
                    os.environ["BL_ENV"] = workspace["env"]

                credentials = workspace.get("credentials", {})
                credentials["workspace"] = workspace_name
                return CredentialsType(
                    workspace=credentials["workspace"],
                    api_key=credentials.get("apiKey"),
                    client_credentials=credentials.get("clientCredentials"),
                    refresh_token=credentials.get("refresh_token"),
                    access_token=credentials.get("access_token"),
                    device_code=credentials.get("device_code"),
                    expires_in=credentials.get("expires_in"),
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
        # Never return None: a sentinel that raises a clear CredentialsError on
        # use keeps `import blaxel` working while turning the old cryptic
        # AttributeError / server-side "workspace is required" into an
        # actionable message.
        return MissingCredentials(base_url, message=_missing_credentials_message())

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


__all__ = [
    "BlaxelAuth",
    "CredentialsError",
    "CredentialsType",
    "MissingCredentials",
    "get_credentials",
    "auth",
]
