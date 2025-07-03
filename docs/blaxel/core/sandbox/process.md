Module blaxel.core.sandbox.process
==================================

Classes
-------

`SandboxProcess(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.action.SandboxAction

    ### Methods

    `exec(self, process: blaxel.core.sandbox.client.models.process_request.ProcessRequest | Dict[str, Any], on_log: Callable[[str], None] | None = None) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :

    `get(self, identifier: str) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :

    `kill(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `list(self) ‑> list[blaxel.core.sandbox.client.models.process_response.ProcessResponse]`
    :

    `logs(self, identifier: str, log_type: Literal['stdout', 'stderr', 'all'] = 'all') ‑> str`
    :

    `stop(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `stream_logs(self, identifier: str, options: Dict[str, Callable[[str], None]] | None = None) ‑> Dict[str, Callable[[], None]]`
    :   Stream logs from a process with callbacks for different output types.

    `wait(self, identifier: str, max_wait: int = 60000, interval: int = 1000) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :   Wait for a process to complete.