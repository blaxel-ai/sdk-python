Module blaxel.core.sandbox.sandbox
==================================

Classes
-------

`SandboxInstance(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   

    ### Static methods

    `create(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxCreateConfiguration | Dict[str, Any] | None = None) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
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

    `wait(self, max_wait: int = 60000, interval: int = 1000) ‑> None`
    :