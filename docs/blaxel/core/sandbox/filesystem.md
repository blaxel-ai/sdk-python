Module blaxel.core.sandbox.filesystem
=====================================

Classes
-------

`SandboxFileSystem(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.action.SandboxAction

    ### Methods

    `cp(self, source: str, destination: str) ‑> blaxel.core.sandbox.types.CopyResponse`
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

    `watch(self, path: str, callback: Callable[[blaxel.core.sandbox.types.WatchEvent], None], options: Dict[str, Any] | None = None) ‑> Dict[str, Callable]`
    :   Watch for file system changes.

    `write(self, path: str, content: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `write_binary(self, path: str, content: bytes | bytearray) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :   Write binary content to a file.

    `write_tree(self, files: List[blaxel.core.sandbox.types.SandboxFilesystemFile | Dict[str, Any]], destination_path: str | None = None) ‑> blaxel.core.sandbox.client.models.directory.Directory`
    :   Write multiple files in a tree structure.