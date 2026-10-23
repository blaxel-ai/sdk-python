import asyncio
import os
import traceback
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack
from logging import getLogger
from typing import Any, TypeVar, cast

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import (
    CallToolRequest,
    CallToolRequestParams,
    CallToolResult,
    ClientRequest,
)
from mcp.types import Tool as MCPTool

from ..client.api.compute.get_sandbox import asyncio as get_sandbox
from ..client.api.functions.get_function import asyncio as get_function
from ..client.client import client
from ..client.models.error import Error
from ..client.types import Unset
from ..common.internal import get_forced_url
from ..common.settings import settings
from .types import Tool

logger = getLogger(__name__)

T = TypeVar("T")

DEFAULT_TIMEOUT = 1
if os.getenv("BL_SERVER_PORT"):
    DEFAULT_TIMEOUT = 5

# JSON-RPC error codes that mean the server-side MCP session is gone and the
# client must reconnect before its next call.
# "Session terminated" is sent by the streamable-HTTP transport when a request
# hits an HTTP 404, i.e. the MCP workload cold-started or the session expired;
# the request is rejected before it reaches the tool, so retrying on a fresh
# session is safe. The mcp library emits this with the (positive) 32600 code,
# so both signs are matched.
_SESSION_TERMINATED_CODES = frozenset({32600, -32600})
# "Connection closed" (-32000) is raised when the transport drops with requests
# in flight; the session is unusable, but the request may have been dispatched,
# so the session is reset without an automatic retry.
_CONNECTION_CLOSED_CODE = -32000


class PersistentMcpClient:
    def __init__(
        self,
        name: str,
        timeout: int = DEFAULT_TIMEOUT,
        timeout_enabled: bool = True,
        transport: str | None = None,
    ):
        self.name = name
        self.timeout = timeout
        self.type = "function"
        self.pluralType = "functions"
        if name.startswith("sandbox/") or name.startswith("sandboxes/"):
            self.name = name.split("/")[1]
            self.type = "sandbox"
            self.pluralType = "sandboxes"
        self.session_exit_stack = AsyncExitStack()
        self.client_exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None
        self.timer_task = None
        self.tools_cache = []
        if settings.bl_cloud:
            self.timeout_enabled = False
        else:
            self.timeout_enabled = timeout_enabled
        self.transport_name = transport
        self.metas = {}
        self._metadata_url: str | None = None

    @property
    def _forced_url(self) -> str | None:
        return get_forced_url(self.type, self.name)

    @property
    def _external_url(self) -> str:
        return f"{settings.run_url}/{settings.workspace}/{self.pluralType}/{self.name}"

    async def _fetch_metadata_url(self) -> str | None:
        """Fetch the resource from the API and return metadata.url if available."""
        try:
            if self.type == "sandbox":
                resource = await get_sandbox(self.name, client=client)
            else:
                resource = await get_function(self.name, client=client)
            if resource and not isinstance(resource, Error) and resource.metadata:
                url = resource.metadata.url
                if not isinstance(url, Unset) and url:
                    return url
        except Exception as e:
            logger.debug(f"Failed to fetch metadata URL for {self.name}: {e}")
        return None

    async def _resolve_url(self) -> str:
        """Resolve the URL: forced > metadata.url > external (run v1 fallback)."""
        if self._forced_url:
            logger.debug(f"Forced URL for {self.name}: {self._forced_url}")
            return self._forced_url

        if self._metadata_url is None:
            self._metadata_url = await self._fetch_metadata_url()

        if self._metadata_url:
            logger.debug(f"Using metadata URL for {self.name}: {self._metadata_url}")
            return self._metadata_url

        logger.debug(f"Falling back to external URL for {self.name}: {self._external_url}")
        return self._external_url

    def with_metas(self, metas: dict[str, Any]):
        self.metas = metas
        return self

    @staticmethod
    def _mcp_error_parts(exc: BaseException) -> tuple[int | None, str]:
        """Extract the JSON-RPC (code, lowercased message) from an exception.

        ``mcp.shared.exceptions.McpError`` carries an ``error`` with ``code`` and
        ``message``; other exceptions fall back to their string form.
        """
        error_data = getattr(exc, "error", None)
        code = getattr(error_data, "code", None) if error_data is not None else None
        message = getattr(error_data, "message", None) if error_data is not None else None
        if not message:
            message = str(exc)
        return (code if isinstance(code, int) else None), message.lower()

    @classmethod
    def _is_session_terminated_error(cls, exc: BaseException) -> bool:
        """True when the server terminated/expired the session.

        The request was rejected before dispatch, so reconnecting and retrying
        once on a fresh session is safe.
        """
        code, message = cls._mcp_error_parts(exc)
        return code in _SESSION_TERMINATED_CODES or "session terminated" in message

    @classmethod
    def _is_stale_session_error(cls, exc: BaseException) -> bool:
        """True when the current session can no longer be used.

        Covers an explicitly terminated session and a closed transport
        connection; either way the client must reconnect before the next call.
        """
        if cls._is_session_terminated_error(exc):
            return True
        code, message = cls._mcp_error_parts(exc)
        return code == _CONNECTION_CLOSED_CODE or "connection closed" in message

    async def _run_with_session_recovery(self, run: Callable[[], Awaitable[T]]) -> T:
        """Run an MCP operation, self-healing a dead session.

        If the operation fails because the server terminated the session or the
        transport was closed, the cached session is dropped so the next call
        reconnects instead of reusing a dead session (which would otherwise fail
        for the lifetime of the process). When the session was explicitly
        terminated — the request never reached the tool — the operation is
        transparently retried once on a fresh session.
        """
        try:
            return await run()
        except Exception as e:
            if not self._is_stale_session_error(e):
                raise
            retryable = self._is_session_terminated_error(e)
            await self._reset_session()
            if not retryable:
                raise
            logger.debug(f"MCP session for {self.name} was terminated; reconnecting and retrying")
            try:
                return await run()
            except Exception:
                await self._reset_session()
                raise

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        try:
            return await self._run_with_session_recovery(
                lambda: self._call_tool_once(tool_name, arguments)
            )
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}\n{traceback.format_exc()}")
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error calling tool {tool_name}: {e}\n{traceback.format_exc()}",
                    }
                ],
                isError=True,
            )

    async def _call_tool_once(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        await self.initialize()
        if self.timeout_enabled:
            self._remove_timer()
        logger.debug(f"Calling tool {tool_name} with arguments {arguments} and meta {self.metas}")

        # Pass meta as a separate field instead of merging into arguments
        # This matches the TypeScript SDK pattern and MCP protocol specification
        call_tool_result = await self.session.send_request(
            ClientRequest(
                CallToolRequest(
                    params=CallToolRequestParams(
                        name=tool_name,
                        arguments=arguments,
                        meta=self.metas if self.metas else None,
                    ),
                )
            ),
            CallToolResult,
        )

        logger.debug(f"Tool {tool_name} returned {call_tool_result}")
        if self.timeout_enabled:
            self._reset_timer()
        else:
            await self._close()
        return call_tool_result

    async def list_tools(self):
        return await self._run_with_session_recovery(self._list_tools_once)

    async def _list_tools_once(self):
        logger.debug(f"Listing tools for {self.name}")
        await self.initialize()
        logger.debug(f"Initialized websocket for {self.name}")
        if self.timeout_enabled:
            self._remove_timer()
        logger.debug("Listing tools")
        list_tools_result = await self.session.list_tools()
        self.tools_cache = list_tools_result.tools
        logger.debug(f"Tools listed: {list_tools_result}")
        if self.timeout_enabled:
            self._reset_timer()
        else:
            await self._close()
        return list_tools_result

    def get_tools(self):
        return self.tools_cache

    async def _get_transport(self):
        """Get the appropriate transport for the connection."""
        url = await self._resolve_url()

        result = await self.client_exit_stack.enter_async_context(
            streamablehttp_client(url + "/mcp", settings.headers)
        )
        return result[0], result[1]

    async def initialize(self):
        if not self.session:
            url = await self._resolve_url()
            logger.debug(f"Initializing client for {url}")
            read, write = await self._get_transport()

            self.session = cast(
                ClientSession,
                await self.session_exit_stack.enter_async_context(ClientSession(read, write)),
            )
            await self.session.initialize()

    def _reset_timer(self):
        self._remove_timer()
        self.timer_task = asyncio.create_task(self._close_after_timeout())

    def _remove_timer(self):
        if self.timer_task:
            self.timer_task.cancel()

    async def _close_after_timeout(self):
        await asyncio.sleep(self.timeout)
        await self._close()
        self.session = None

    async def _close(self):
        logger.debug(f"Closing client for {self.name}")
        if self.session:
            await self._teardown()
            logger.debug("WebSocket connection closed due to inactivity.")

    async def _reset_session(self):
        """Drop the current session and transport so the next call reconnects
        with a fresh session. Safe to call when no session is open."""
        self._remove_timer()
        await self._teardown()

    async def _teardown(self):
        """Close the session and transport exit stacks and clear the session."""
        self.session = None
        # Swap exit stacks to fresh ones BEFORE closing the old ones.
        # This prevents a race where initialize() runs during the await
        # and pushes new contexts onto stacks that are being closed.
        old_session_stack = self.session_exit_stack
        old_client_stack = self.client_exit_stack
        self.session_exit_stack = AsyncExitStack()
        self.client_exit_stack = AsyncExitStack()
        try:
            await old_session_stack.aclose()
        except Exception as e:
            logger.debug(f"Error closing session exit stack: {e}")
        try:
            await old_client_stack.aclose()
        except Exception as e:
            logger.debug(f"Error closing client exit stack: {e}")


def convert_mcp_tool_to_blaxel_tool(
    mcp_client: PersistentMcpClient,
    tool: MCPTool,
) -> Tool:
    """Convert an MCP tool to a blaxel tool.

    NOTE: this tool can be executed only in a context of an active MCP client session.

    Args:
        session: MCP client session
        tool: MCP tool to convert

    Returns:
        a LangChain tool
    """

    async def initialize_and_call_tool(
        *args: Any,
        **arguments: dict[str, Any],
    ) -> CallToolResult:
        logger.debug(f"Calling tool {tool.name} with arguments {arguments}")
        call_tool_result = await mcp_client.call_tool(tool.name, arguments)
        logger.debug(f"Tool {tool.name} returned {call_tool_result}")
        return call_tool_result

    async def call_tool(
        *args: Any,
        **arguments: dict[str, Any],
    ) -> CallToolResult:
        return await initialize_and_call_tool(*args, **arguments)

    def sync_call_tool(*args: Any, **arguments: dict[str, Any]) -> CallToolResult:
        try:
            loop = asyncio.get_running_loop()
            return loop.run_until_complete(initialize_and_call_tool(*args, **arguments))
        except RuntimeError:
            return asyncio.run(initialize_and_call_tool(*args, **arguments))

    return Tool(
        name=tool.name,
        description=tool.description or "",
        input_schema=tool.inputSchema,
        coroutine=call_tool,
        sync_coroutine=sync_call_tool,
        response_format="content_and_artifact",
    )


toolPersistances: dict[str, PersistentMcpClient] = {}


class BlTools:
    def __init__(
        self,
        functions: list[str],
        metas: dict[str, Any] = {},
        timeout: int = DEFAULT_TIMEOUT,
        timeout_enabled: bool = True,
        transport: str = None,
    ):
        self.functions = functions
        self.metas = metas
        self.timeout = timeout
        self.timeout_enabled = timeout_enabled
        self.transport = transport

    def get_tools(self) -> list[Tool]:
        """Get a list of all tools from all connected servers."""
        all_tools: list[Tool] = []
        for name in self.functions:
            toolPersistances.get(name).with_metas(self.metas)
            websocket = toolPersistances.get(name)
            tools = websocket.get_tools()
            converted_tools = [convert_mcp_tool_to_blaxel_tool(websocket, tool) for tool in tools]
            all_tools.extend(converted_tools)
        return all_tools

    async def connect(self, name: str):
        # Create and store the connection
        logger.debug("Initializing session and loading tools")

        if not toolPersistances.get(name):
            logger.debug(f"Creating new persistent connection for {name}")
            toolPersistances[name] = PersistentMcpClient(
                name,
                timeout=self.timeout,
                timeout_enabled=self.timeout_enabled,
                transport=self.transport,
            )
            await toolPersistances[name].list_tools()
        logger.debug(f"Loaded {len(toolPersistances[name].get_tools())} tools")
        return toolPersistances[name].with_metas(self.metas)

    async def initialize(self) -> "BlTools":
        for i in range(0, len(self.functions), 10):
            batch = self.functions[i : i + 10]
            await asyncio.gather(*(self.connect(name) for name in batch))
        return self


def bl_tools(
    functions: list[str],
    metas: dict[str, Any] = {},
    timeout: int = DEFAULT_TIMEOUT,
    timeout_enabled: bool = True,
    transport: str = None,
) -> BlTools:
    return BlTools(
        functions,
        metas=metas,
        timeout=timeout,
        timeout_enabled=timeout_enabled,
        transport=transport,
    )
