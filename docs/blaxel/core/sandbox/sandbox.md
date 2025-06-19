Module blaxel.core.sandbox.sandbox
==================================

Classes
-------

`SandboxInstance(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   

    ### Static methods

    `create(sandbox: blaxel.core.client.models.sandbox.Sandbox) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

    `delete(sandbox_name: str) ‑> blaxel.core.client.models.sandbox.Sandbox`
    :

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