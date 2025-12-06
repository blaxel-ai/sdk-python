from ...common.settings import settings
from ..client.api.codegen.get_codegen_reranking_path import (
    asyncio as get_codegen_reranking_path,
)
from ..client.api.fastapply.put_codegen_fastapply_path import (
    asyncio as put_codegen_fastapply_path,
)
from ..client.client import Client
from ..client.models import (
    ApplyEditRequest,
    ApplyEditResponse,
    ErrorResponse,
    RerankingResponse,
)
from ..types import SandboxConfiguration
from .action import SandboxAction


class SandboxCodegen(SandboxAction):
    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    async def fastapply(
        self, path: str, code_edit: str, model: str | None = None
    ) -> ApplyEditResponse:
        """Apply a code edit to a file using the configured LLM provider.

        Args:
            path: The path to the file to edit
            code_edit: The code edit to apply
            model: Optional model to use for the edit

        Returns:
            ApplyEditResponse with the result of the edit
        """
        body = ApplyEditRequest(code_edit=code_edit, model=model)

        # Create a Client instance with the sandbox URL and headers
        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        async with client:
            response = await put_codegen_fastapply_path(
                path=path,
                body=body,
                client=client,
            )
            if response is None:
                raise Exception("Failed to apply code edit")
            if isinstance(response, ErrorResponse):
                raise Exception(f"Code edit failed: {response}")
            return response

    async def reranking(
        self,
        path: str,
        query: str,
        score_threshold: float | None = None,
        token_limit: int | None = None,
        file_pattern: str | None = None,
    ) -> RerankingResponse:
        """Perform code reranking/semantic search on files.

        Args:
            path: The base path to search in
            query: The search query
            score_threshold: Minimum score threshold for results
            token_limit: Maximum token limit for results
            file_pattern: Optional file pattern to filter results

        Returns:
            RerankingResponse with ranked files
        """
        # Create a Client instance with the sandbox URL and headers
        client = Client(
            base_url=self.url,
            headers={**settings.headers, **self.sandbox_config.headers},
        )

        async with client:
            response = await get_codegen_reranking_path(
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
