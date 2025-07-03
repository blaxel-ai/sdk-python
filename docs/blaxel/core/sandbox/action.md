Module blaxel.core.sandbox.action
=================================

Classes
-------

`ResponseError(response: httpx.Response, data: Any = None, error: Any = None)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`SandboxAction(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Descendants

    * blaxel.core.sandbox.filesystem.SandboxFileSystem
    * blaxel.core.sandbox.network.SandboxNetwork
    * blaxel.core.sandbox.process.SandboxProcess

    ### Instance variables

    `external_url: str`
    :

    `fallback_url: str | None`
    :

    `forced_url: str | None`
    :

    `internal_url: str`
    :

    `name: str`
    :

    `url: str`
    :

    ### Methods

    `get_client(self) ‑> httpx.AsyncClient`
    :

    `handle_response_error(self, response: httpx.Response, data: Any, error: Any)`
    :