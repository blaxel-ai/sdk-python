Module blaxel.core.sandbox.process
==================================

Classes
-------

`SandboxProcess(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.base.SandboxHandleBase

    ### Methods

    `exec(self, process: blaxel.core.sandbox.client.models.process_request.ProcessRequest) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :

    `get(self, identifier: str) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :

    `kill(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `list(self) ‑> list[blaxel.core.sandbox.client.models.process_response.ProcessResponse]`
    :

    `logs(self, identifier: str, type_: str = 'stdout') ‑> str`
    :

    `stop(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :