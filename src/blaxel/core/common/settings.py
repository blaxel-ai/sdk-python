import os
import platform
from pathlib import Path
from typing import Dict

import yaml

from ..authentication import BlaxelAuth, auth
from .logger import init_logger


def _get_os_arch() -> str:
    """Get OS and architecture information."""
    try:
        system = platform.system().lower()
        if system == "windows":
            os_name = "windows"
        elif system == "darwin":
            os_name = "darwin"
        elif system == "linux":
            os_name = "linux"
        else:
            os_name = system

        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            arch = "amd64"
        elif machine in ["aarch64", "arm64"]:
            arch = "arm64"
        elif machine in ["i386", "i686", "x86"]:
            arch = "386"
        else:
            arch = machine

        return f"{os_name}/{arch}"
    except Exception:
        return "unknown/unknown"


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
    def sentry_dsn(self) -> str:
        """Get the Sentry DSN (injected at build time)."""
        import blaxel

        return blaxel.__sentry_dsn__

    @property
    def version(self) -> str:
        """Get the package version (injected at build time)."""
        import blaxel

        return blaxel.__version__ or "unknown"

    @property
    def commit(self) -> str:
        """Get the commit hash (injected at build time)."""
        import blaxel

        return blaxel.__commit__ or "unknown"

    @property
    def headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        headers = self.auth.get_headers()
        os_arch = _get_os_arch()
        headers["User-Agent"] = f"blaxel/sdk/python/{self.version} ({os_arch}) blaxel/{self.commit}"
        return headers

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
        if self.generation == "":
            return ""
        return os.environ.get("BL_RUN_INTERNAL_HOST", "")

    @property
    def generation(self) -> str:
        """Get the generation."""
        return os.environ.get("BL_GENERATION", "")

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

    @property
    def tracking(self) -> bool:
        """
        Get the tracking setting.

        Priority:
        1. Environment variable DO_NOT_TRACK (true/1 to disable, false/0 to enable)
        2. config.yaml tracking field
        3. Default: true
        """
        env_value = os.environ.get("DO_NOT_TRACK")
        if env_value is not None:
            return env_value.lower() not in ("true", "1")

        try:
            home_dir = Path.home()
            config_path = home_dir / ".blaxel" / "config.yaml"
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if config and "tracking" in config:
                return bool(config["tracking"])
        except Exception:
            pass

        return True


settings = Settings()
