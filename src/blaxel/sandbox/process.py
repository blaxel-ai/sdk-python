from blaxel.sandbox.client.models.process_request import ProcessRequest

from .base import SandboxHandleBase
from .client.api.process.delete_process_identifier import (
    asyncio_detailed as delete_process_by_identifier,
)
from .client.api.process.delete_process_identifier_kill import (
    asyncio_detailed as delete_process_by_identifier_kill,
)
from .client.api.process.get_process import asyncio_detailed as get_process
from .client.api.process.get_process_identifier import asyncio_detailed as get_process_by_identifier
from .client.api.process.get_process_identifier_logs import (
    asyncio_detailed as get_process_by_identifier_logs,
)
from .client.api.process.post_process import asyncio_detailed as post_process
from .client.models import (
    GetProcessIdentifierLogsResponse200,
    ProcessKillRequest,
    ProcessResponse,
    SuccessResponse,
)


class SandboxProcess(SandboxHandleBase):
    async def exec(self, process: ProcessRequest) -> ProcessResponse:
        response = await post_process(client=self.client, body=process)
        self.handle_response(response)
        return response.parsed

    async def get(self, identifier: str) -> ProcessResponse:
        response = await get_process_by_identifier(identifier=identifier, client=self.client)
        self.handle_response(response)
        return response.parsed

    async def list(self) -> list[ProcessResponse]:
        response = await get_process(client=self.client)
        self.handle_response(response)
        return response.parsed

    async def stop(self, identifier: str) -> SuccessResponse:
        response = await delete_process_by_identifier(identifier=identifier, client=self.client)
        self.handle_response(response)
        return response.parsed

    async def kill(self, identifier: str, signal: str = "SIGKILL") -> SuccessResponse:
        kill_request = ProcessKillRequest(signal=signal)
        response = await delete_process_by_identifier_kill(identifier=identifier, client=self.client, body=kill_request)
        self.handle_response(response)
        return response.parsed

    async def logs(self, identifier: str, type_: str = "stdout") -> str:
        response = await get_process_by_identifier_logs(identifier=identifier, client=self.client)
        self.handle_response(response)
        data: GetProcessIdentifierLogsResponse200 = response.parsed
        if type_ in data.additional_properties:
            return data.additional_properties[type_]
        raise Exception("Unsupported log type")
