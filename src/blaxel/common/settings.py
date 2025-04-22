import os
from typing import Dict

from ..authentication import BlaxelAuth, auth
from .logger import init_logger


class Settings:
    auth: BlaxelAuth

    def __init__(self):
        init_logger(self.log_level)
        self.auth = auth(self.env, self.base_url)
        self._headers = None

    @property
    def env(self) -> str:
        """Get the environment."""
        return os.environ.get("BL_ENV", "prod")

    @property
    def log_level(self) -> str:
        """Get the log level."""
        return os.environ.get("LOG_LEVEL", "INFO").upper()

    @property
    def base_url(self) -> str:
        """Get the base URL for the API."""
        if self.env == "prod":
            return "https://api.blaxel.ai/v0"
        return "https://api.blaxel.dev/v0"

    @property
    def run_url(self) -> str:
        """Get the run URL."""
        if self.env == "prod":
            return "https://run.blaxel.ai"
        return "https://run.blaxel.dev"


    @property
    def headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        return self.auth.get_headers()


    @property
    def name(self) -> str:
        """Get the name."""
        return os.environ.get("BL_NAME", "")

    @property
    def type(self) -> str:
        """Get the type."""
        return os.environ.get("BL_TYPE", "agent")

    @property
    def workspace(self) -> str:
        """Get the workspace."""
        return self.auth.workspace_name

    @property
    def run_internal_hostname(self) -> str:
        """Get the run internal hostname."""
        return os.environ.get("BL_RUN_INTERNAL_HOSTNAME", "")

    @property
    def bl_cloud(self) -> bool:
        """Is running on bl cloud."""
        return os.environ.get("BL_CLOUD", "") == "true"

    @property
    def run_internal_protocol(self) -> str:
        """Get the run internal protocol."""
        return os.environ.get("BL_RUN_INTERNAL_PROTOCOL", "https")

    @property
    def enable_opentelemetry(self) -> bool:
        """Get the enable opentelemetry."""
        return os.getenv("BL_ENABLE_OPENTELEMETRY", "false").lower() == "true"

settings = Settings()
