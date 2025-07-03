Module blaxel.core.sandbox.session
==================================

Classes
-------

`SandboxSessions(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Instance variables

    `sandbox_name: str`
    :

    ### Methods

    `create(self, options: blaxel.core.sandbox.types.SessionCreateOptions | Dict[str, Any] | None = None) ‑> blaxel.core.sandbox.types.SessionWithToken`
    :

    `create_if_expired(self, options: blaxel.core.sandbox.types.SessionCreateOptions | Dict[str, Any] | None = None, delta_seconds: int = 3600) ‑> blaxel.core.sandbox.types.SessionWithToken`
    :

    `delete(self, name: str)`
    :

    `get(self, name: str) ‑> blaxel.core.sandbox.types.SessionWithToken`
    :

    `get_token(self, preview_name: str)`
    :

    `list(self) ‑> List[blaxel.core.sandbox.types.SessionWithToken]`
    :