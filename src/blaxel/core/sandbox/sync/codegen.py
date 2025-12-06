from ...common.settings import settings
from ..client.api.codegen.get_codegen_reranking_path import (
    sync as get_codegen_reranking_path,
)
from ..client.api.fastapply.put_codegen_fastapply_path import (
    sync as put_codegen_fastapply_path,
)
from ..client.client import Client
from ..client.models import (
    ApplyEditRequest,
    ApplyEditResponse,
    ErrorResponse,
    RerankingResponse,
)
from ..types import SandboxConfiguration
from .action import SyncSandboxAction


class SyncSandboxCodegen(SyncSandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    def fastapply(self, path: str, code_edit: str, model: str | None = None) -> ApplyEditResponse:
        body = ApplyEditRequest(code_edit=code_edit, model=model)
        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )
        with client:
            response = put_codegen_fastapply_path(
                path=path,
                body=body,
                client=client,
            )
            if response is None:
                raise Exception("Failed to apply code edit")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Code edit failed: {response}")
            return response

    def reranking(
        self,
        path: str,
        query: str,
        score_threshold: float | None = None,
        token_limit: int | None = None,
        file_pattern: str | None = None,
    ) -> RerankingResponse:
        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )
        with client:
            response = get_codegen_reranking_path(
                path=path,
                query=query,
                score_threshold=score_threshold,
                token_limit=token_limit,
                file_pattern=file_pattern,
                client=client,
            )
            if response is None:
                raise Exception("Failed to get reranking results")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Reranking failed: {response}")
            return response
