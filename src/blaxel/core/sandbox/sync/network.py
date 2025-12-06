from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxNetwork(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    # Placeholder for future sync network operations
