Module blaxel.core.sandbox.base
===============================

Classes
-------

`ResponseError(response: httpx.Response)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`SandboxHandleBase(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   

    ### Descendants

    * blaxel.core.sandbox.filesystem.SandboxFileSystem
    * blaxel.core.sandbox.process.SandboxProcess

    ### Instance variables

    `external_url`
    :

    `fallback_url`
    :

    `forced_url`
    :

    `internal_url`
    :

    `name`
    :

    `url`
    :

    ### Methods

    `handle_response(self, response: httpx.Response)`
    :