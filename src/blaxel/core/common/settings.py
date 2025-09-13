import os
import platform
from pathlib import Path
from typing import Dict

import tomli

from ..authentication import BlaxelAuth, auth
from .logger import init_logger


def _get_package_version() -> str:
    """Get the package version from pyproject.toml."""
    try:
        # Navigate up from this file to the project root
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
                return pyproject_data.get("project", {}).get("version", "unknown")
        else:
            return "unknown"
    except Exception as e:
        print(f"Warning: Failed to read package version: {e}")
        return "unknown"


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


def _get_commit_hash() -> str:
    """Get commit hash from pyproject.toml."""
    try:
        # Try to read from pyproject.toml (build-time injection)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
                # Check multiple possible locations for commit
                commit = None
                if "tool" in pyproject_data and "blaxel" in pyproject_data["tool"]:
                    commit = pyproject_data["tool"]["blaxel"].get("commit")
                if not commit and "project" in pyproject_data:
                    commit = pyproject_data["project"].get("commit")
                if not commit and "build" in pyproject_data:
                    commit = pyproject_data["build"].get("commit")
                    
                if commit:
                    return commit[:7] if len(commit) > 7 else commit
    except Exception:
        pass
    
    return "unknown"

class Settings:
    auth: BlaxelAuth

    def __init__(self):
        init_logger(self.log_level)
        self.auth = auth(self.env, self.base_url)
        self._headers = None
        self._version = None

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
    def version(self) -> str:
        """Get the package version."""
        if self._version is None:
            self._version = _get_package_version()
        return self._version

    @property
    def headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        headers = self.auth.get_headers()
        os_arch = _get_os_arch()
        commit_hash = _get_commit_hash()
        headers["User-Agent"] = f"blaxel/sdk/python/{self.version} ({os_arch}) blaxel/{commit_hash}"
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
    def workspace_id(self) -> str:
        """Get the workspace ID for cloud environments."""
        return os.environ.get("BL_WORKSPACE_ID", "")

    @property
    def run_internal_protocol(self) -> str:
        """Get the run internal protocol."""
        return os.environ.get("BL_RUN_INTERNAL_PROTOCOL", "https")

    @property
    def enable_opentelemetry(self) -> bool:
        """Get the enable opentelemetry."""
        return os.getenv("BL_ENABLE_OPENTELEMETRY", "false").lower() == "true"

settings = Settings()
