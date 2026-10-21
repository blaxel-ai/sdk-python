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
    """Edit and search code with an LLM provider configured in the sandbox.

    Reach it as ``sandbox.codegen``. The sandbox needs ``RELACE_API_KEY`` or
    ``MORPH_API_KEY`` in its environment (set it in ``envs`` when creating the
    sandbox). Without either key the sandbox API answers HTTP 400 ("codegen
    tools are not configured"); :meth:`reranking` also needs
    ``RELACE_API_KEY`` and answers HTTP 503 with only ``MORPH_API_KEY``. Errors
    raise a plain ``Exception`` whose message holds the API error.

    Example:
        ```python
        envs = [{"name": "RELACE_API_KEY", "value": os.environ["RELACE_API_KEY"]}]
        sandbox = await SandboxInstance.create({"name": "coder", "envs": envs})
        edit = "// ... existing code ...\\nprint('done')\\n"
        await sandbox.codegen.fastapply("/app/main.py", edit)
        ```
    """

    def __init__(self, sandbox_config: SandboxConfiguration):
        super().__init__(sandbox_config)

    async def fastapply(
        self, path: str, code_edit: str, model: str | None = None
    ) -> ApplyEditResponse:
        """Apply a code edit to a file using the configured LLM provider.

        The provider merges ``code_edit`` into the current file and the result
        is written back to ``path``; a missing file is created from the edit.
        In ``code_edit``, mark unchanged spans with
        ``// ... existing code ...`` and keep a few unchanged lines around each
        change so the provider can place it.

        Args:
            path: The path to the file to edit
            code_edit: The code edit to apply
            model: Optional model to use for the edit

        Returns:
            ApplyEditResponse with the result of the edit (``success``,
            ``original_content``, ``updated_content`` and ``provider``)

        Raises:
            Exception: When no provider is configured, the request is invalid
                or the provider fails.
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

        Ranks the files under ``path`` by relevance to ``query``, most
        relevant first. Needs ``RELACE_API_KEY`` in the sandbox. Suggested
        starting values are ``score_threshold=0.5`` and ``token_limit=30000``.

        Args:
            path: The base path to search in
            query: The search query
            score_threshold: Minimum score threshold for results
            token_limit: Maximum token limit for results
            file_pattern: Optional file pattern to filter results (a regular
                expression, such as ``.*\\.py$``)

        Returns:
            RerankingResponse with ranked files (``files`` with ``path``,
            ``score`` and ``content``)

        Raises:
            Exception: When Relace is not configured, the request is invalid or
                the provider fails.
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
