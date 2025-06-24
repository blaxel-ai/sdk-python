Module blaxel.core.sandbox.filesystem
=====================================

Classes
-------

`SandboxFileSystem(sandbox)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.base.SandboxHandleBase

    ### Methods

    `cp(self, source: str, destination: str) ‑> Dict[str, str]`
    :

    `format_path(self, path: str) ‑> str`
    :

    `ls(self, path: str) ‑> blaxel.core.sandbox.client.models.directory.Directory`
    :

    `mkdir(self, path: str, permissions: str = '0755') ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `read(self, path: str) ‑> str`
    :

    `rm(self, path: str, recursive: bool = False) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `write(self, path: str, content: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :