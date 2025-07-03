Module blaxel.core.sandbox.types
================================

Classes
-------

`CopyResponse(message: str, source: str, destination: str)`
:   

`SandboxConfiguration(sandbox: blaxel.core.client.models.sandbox.Sandbox, force_url: str | None = None, headers: Dict[str, str] | None = None, params: Dict[str, str] | None = None)`
:   

    ### Instance variables

    `metadata`
    :

    `spec`
    :

    `status`
    :

`SandboxCreateConfiguration(name: str | None = None, image: str | None = None, memory: int | None = None, ports: List[blaxel.core.client.models.port.Port] | List[Dict[str, Any]] | None = None, envs: List[Dict[str, str]] | None = None)`
:   Simplified configuration for creating sandboxes with default values.

    ### Static methods

    `from_dict(data: Dict[str, Any]) ‑> blaxel.core.sandbox.types.SandboxCreateConfiguration`
    :

`SandboxFilesystemFile(path: str, content: str)`
:   

    ### Static methods

    `from_dict(data: Dict[str, Any]) ‑> blaxel.core.sandbox.types.SandboxFilesystemFile`
    :

`SessionCreateOptions(expires_at: datetime.datetime | None = None, response_headers: Dict[str, str] | None = None, request_headers: Dict[str, str] | None = None)`
:   

    ### Static methods

    `from_dict(data: Dict[str, Any]) ‑> blaxel.core.sandbox.types.SessionCreateOptions`
    :

`SessionWithToken(name: str, url: str, token: str, expires_at: datetime.datetime)`
:   

    ### Static methods

    `from_dict(data: Dict[str, Any]) ‑> blaxel.core.sandbox.types.SessionWithToken`
    :

`WatchEvent(op: str, path: str, name: str, content: str | None = None)`
: