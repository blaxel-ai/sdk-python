import asyncio
import os
import traceback
from contextlib import AsyncExitStack
from logging import getLogger
from typing import Any, cast

from mcp import ClientSession
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool

from ..common.internal import generate_internal_url, get_forced_url
from ..common.settings import settings
from ..mcp.client import websocket_client
from .types import Tool

logger = getLogger(__name__)

DEFAULT_TIMEOUT = 1
if os.getenv("BL_SERVER_PORT"):
    DEFAULT_TIMEOUT = 5


class PersistentWebSocket:
    def __init__(self, name: str, timeout: int = DEFAULT_TIMEOUT, timeout_enabled: bool = True):
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
        self.session: ClientSession = None
        self.timer_task = None
        self.tools_cache = []
        if settings.bl_cloud:
            self.timeout_enabled = False
        else:
            self.timeout_enabled = timeout_enabled
        self.use_fallback_url = False

    @property
    def _internal_url(self):
        """Get the internal URL for the tool/function/mcp."""
        return generate_internal_url(
            settings.workspace,
            self.type,
            self.name,
            settings.env,
            settings.run_internal_protocol,
            settings.run_internal_hostname,
            settings.bl_cloud,
            settings.workspace_id
        )

    @property
    def _forced_url(self):
        """Get the forced URL from environment variables if set."""
        return get_forced_url(self.type, self.name)

    @property
    def _external_url(self):
        return f"{settings.run_url}/{settings.workspace}/{self.pluralType}/{self.name}"

    @property
    def _fallback_url(self):
        # Compute the primary URL without fallback to avoid recursion
        primary_url = self._external_url  # default
        if self._forced_url:
            primary_url = self._forced_url
        elif settings.run_internal_hostname:
            primary_url = self._internal_url

        if self._external_url != primary_url:
            return self._external_url
        return None

    @property
    def _url(self):
        if self.use_fallback_url:
            return self._fallback_url
        logger.debug(f"Getting URL for {self.name}")
        if self._forced_url:
            logger.debug(f"Forced URL found for {self.name}: {self._forced_url}")
            return self._forced_url
        if settings.run_internal_hostname:
            logger.debug(f"Internal hostname found for {self.name}: {self._internal_url}")
            return self._internal_url
        logger.debug(f"No URL found for {self.name}, using external URL")
        return self._external_url

    def with_metas(self, metas: dict[str, Any]):
        self.metas = metas
        return self

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        try:
            await self.initialize()
            if self.timeout_enabled:
                self._remove_timer()
            logger.debug(f"Calling tool {tool_name} with arguments {arguments}")
            arguments.update(self.metas)
            call_tool_result = await self.session.call_tool(tool_name, arguments)
            logger.debug(f"Tool {tool_name} returned {call_tool_result}")
            if self.timeout_enabled:
                self._reset_timer()
            else:
                await self._close()
            return call_tool_result
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

    async def list_tools(self):
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

    async def initialize(self, fallback: bool = False):
        if not self.session:
            try:
                logger.debug(f"Initializing websocket client for {self._url}")
                read, write = await self.client_exit_stack.enter_async_context(
                    websocket_client(self._url, settings.headers)
                )
                self.session = cast(
                    ClientSession,
                    await self.session_exit_stack.enter_async_context(ClientSession(read, write)),
                )
                await self.session.initialize()
            except Exception as e:
                if not fallback and self._fallback_url is not None:
                    self.use_fallback_url = True
                    return await self.initialize(fallback=True)
                raise e

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
        logger.debug(f"Closing websocket client {self._url}")
        if self.session:
            self.session = None
            try:
                await self.session_exit_stack.aclose()
            except Exception as e:
                logger.debug(f"Error closing session exit stack: {e}")
            try:
                await self.client_exit_stack.aclose()
            except Exception as e:
                logger.debug(f"Error closing client exit stack: {e}")
            logger.debug("WebSocket connection closed due to inactivity.")


def convert_mcp_tool_to_blaxel_tool(
    websocket_client: PersistentWebSocket,
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
        call_tool_result = await websocket_client.call_tool(tool.name, arguments)
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


toolPersistances: dict[str, PersistentWebSocket] = {}


class BlTools:
    def __init__(
        self,
        functions: list[str],
        metas: dict[str, Any] = {},
        timeout: int = DEFAULT_TIMEOUT,
        timeout_enabled: bool = True,
    ):
        self.functions = functions
        self.metas = metas
        self.timeout = timeout
        self.timeout_enabled = timeout_enabled

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
            logger.debug(f"Creating new persistent websocket for {name}")
            toolPersistances[name] = PersistentWebSocket(
                name, timeout=self.timeout, timeout_enabled=self.timeout_enabled
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
) -> BlTools:
    return BlTools(functions, metas=metas, timeout=timeout, timeout_enabled=timeout_enabled)
