from .action import SandboxAction
from .types import SandboxConfiguration


class SandboxNetwork(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    # Network functionality can be expanded here in the future
    # Currently this is a placeholder matching the TypeScript implementation
