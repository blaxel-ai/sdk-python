Module blaxel.core.sandbox.sandbox
==================================

Classes
-------

`SandboxInstance(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxConfiguration, force_url: str | None = None, headers: Dict[str, str] | None = None, params: Dict[str, str] | None = None)`
:   

    ### Static methods

    `create(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxCreateConfiguration | Dict[str, Any] | None = None, safe: bool = True) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

    `create_if_not_exists(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxCreateConfiguration | Dict[str, Any]) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Create a sandbox if it doesn't exist, otherwise return existing.

    `delete(sandbox_name: str) ‑> blaxel.core.client.models.sandbox.Sandbox`
    :

    `from_session(session: blaxel.core.sandbox.types.SessionWithToken | Dict[str, Any]) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Create a sandbox instance from a session with token.

    `get(sandbox_name: str) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

    `list() ‑> List[blaxel.core.sandbox.sandbox.SandboxInstance]`
    :

    `update_metadata(sandbox_name: str, metadata: blaxel.core.sandbox.types.SandboxUpdateMetadata) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Update sandbox metadata by merging new metadata with existing metadata.
        
        Args:
            sandbox_name: The name of the sandbox to update
            metadata: The metadata fields to update (labels and/or display_name)
        
        Returns:
            A new SandboxInstance with updated metadata

    ### Instance variables

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `wait(self, max_wait: int = 60000, interval: int = 1000) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :