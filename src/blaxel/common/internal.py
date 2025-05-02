import base64
import hashlib
import os
import re
from logging import getLogger
from typing import Optional

logger = getLogger(__name__)

def get_alphanumeric_limited_hash(input_str, max_size):
    # Create SHA-256 hash of the input string
    hash_obj = hashlib.sha256(input_str.encode('utf-8'))

    # Get the hash digest in base64 format
    hash_base64 = base64.b64encode(hash_obj.digest()).decode('utf-8')

    # Remove non-alphanumeric characters and convert to lowercase
    alphanumeric = re.sub(r'[^a-zA-Z0-9]', '', hash_base64).lower()

    # Skip the first character to match the Node.js crypto output
    alphanumeric = alphanumeric[1:]

    # Limit to max_size characters
    return alphanumeric[:max_size] if len(alphanumeric) > max_size else alphanumeric


def get_global_unique_hash(workspace: str, type: str, name: str) -> str:
    """
    Generate a unique hash for a combination of workspace, type, and name.

    Args:
        workspace: The workspace identifier
        type: The type identifier
        name: The name identifier

    Returns:
        A unique alphanumeric hash string of maximum length 48
    """
    global_unique_name = f"{workspace}-{type}-{name}"
    hash = get_alphanumeric_limited_hash(global_unique_name, 48)
    return hash

class Agent:
    def __init__(self, agent_name: str, workspace: str, run_internal_protocol: str, run_internal_hostname: str):
        self.agent_name = agent_name
        self.workspace = workspace
        self.run_internal_protocol = run_internal_protocol
        self.run_internal_hostname = run_internal_hostname

    @property
    def internal_url(self) -> str:
        """
        Generate the internal URL for the agent using a unique hash.

        Returns:
            The internal URL as a string
        """
        hash_value = get_global_unique_hash(
            self.workspace,
            "agent",
            self.agent_name
        )
        return f"{self.run_internal_protocol}://{hash_value}.{self.run_internal_hostname}"

    @property
    def forced_url(self) -> Optional[str]:
        """
        Check for a forced URL in environment variables.

        Returns:
            The forced URL if found in environment variables, None otherwise
        """
        env_var = self.agent_name.replace("-", "_").upper()
        env_key = f"BL_AGENT_{env_var}_URL"
        return os.environ.get(env_key)
