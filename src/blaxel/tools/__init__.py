import asyncio
import json
import os
import traceback
from contextlib import AsyncExitStack
from logging import getLogger
from typing import Any, cast

from mcp import ClientSession
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool

from ..common.env import env
from ..common.internal import get_global_unique_hash
from ..common.settings import settings
from ..instrumentation.span import SpanManager
from ..mcp.client import websocket_client
from .types import Tool

logger = getLogger(__name__)

DEFAULT_TIMEOUT = 1
if os.getenv("BL_SERVER_PORT"):
    DEFAULT_TIMEOUT = 5

class PersistentWebSocket:
    def __init__(self, url: str, name: str, timeout: int = DEFAULT_TIMEOUT, timeout_enabled: bool = True):
        self.url = url
        self.name = name
        self.timeout = timeout
        self.session_exit_stack = AsyncExitStack()
        self.client_exit_stack = AsyncExitStack()
        self.session: ClientSession = None
        self.timer_task = None
        self.tools_cache = []
        if settings.bl_cloud:
            self.timeout_enabled = False
        else:
            self.timeout_enabled = timeout_enabled

    def with_metas(self, metas: dict[str, Any]):
        self.metas = metas
        return self

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        await self._initialize()
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

    async def list_tools(self):
        logger.debug(f"Listing tools for {self.name}")
        span_attributes = {
            "tool.server": self.url,
            "tool.server_name": self.name,
            "span.type": "tool.list",
        }
        with SpanManager("blaxel-tracer").create_active_span(self.name, span_attributes) as span:
            await self._initialize()
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
            span.set_attribute("tool.list.result", list_tools_result.model_dump_json())
            return list_tools_result

    def get_tools(self):
        return self.tools_cache

    async def _initialize(self):
        if not self.session:
            logger.debug(f"Initializing websocket client for {self.url}")
            read, write = await self.client_exit_stack.enter_async_context(websocket_client(self.url, settings.headers))
            self.session = cast(ClientSession, await self.session_exit_stack.enter_async_context(ClientSession(read, write)))
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
        logger.debug(f"Closing websocket client {self.url}")
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
    name: str,
    url: str,
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
        span_attributes = {
            "tool.name": tool.name,
            "tool.args": json.dumps(arguments),
            "tool.server": url,
            "tool.server_name": name,
            "span.type": "tool.call",
        }
        with SpanManager("blaxel-tracer").create_active_span("blaxel-tool-call", span_attributes):
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
    def __init__(self, functions: list[str], metas: dict[str, Any] = {}, timeout: int = DEFAULT_TIMEOUT, timeout_enabled: bool = True):
        self.functions = functions
        self.metas = metas
        self.timeout = timeout
        self.timeout_enabled = timeout_enabled

    def _internal_url(self, name: str):
        """Get the internal URL for the agent using a hash of workspace and agent name."""
        hash = get_global_unique_hash(settings.workspace, "function", name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash}.{settings.run_internal_hostname}"

    def _forced_url(self, name: str):
        """Get the forced URL from environment variables if set."""
        env_var = name.replace("-", "_").upper()
        if env[f"BL_FUNCTION_{env_var}_URL"]:
            return env[f"BL_FUNCTION_{env_var}_URL"]
        return None

    def _external_url(self, name: str):
        return f"{settings.run_url}/{settings.workspace}/functions/{name}"

    def _fallback_url(self, name: str):
        if self._external_url(name) != self._url(name):
            return self._external_url(name)
        return None

    def _url(self, name: str):
        logger.debug(f"Getting URL for {name}")
        if self._forced_url(name):
            logger.debug(f"Forced URL found for {name}: {self._forced_url(name)}")
            return self._forced_url(name)
        if settings.run_internal_hostname:
            logger.debug(f"Internal hostname found for {name}: {self._internal_url(name)}")
            return self._internal_url(name)
        logger.debug(f"No URL found for {name}, using external URL")
        return self._external_url(name)

    def get_tools(self) -> list[Tool]:
        """Get a list of all tools from all connected servers."""
        all_tools: list[Tool] = []
        for name in self.functions:
            toolPersistances.get(name).with_metas(self.metas)
            websocket = toolPersistances.get(name)
            tools = websocket.get_tools()
            converted_tools = [convert_mcp_tool_to_blaxel_tool(websocket, name, self._url(name), tool) for tool in tools]
            all_tools.extend(converted_tools)
        return all_tools

    async def to_langchain(self):
        from .langchain import get_langchain_tools

        await self.initialize()
        return get_langchain_tools(self.get_tools())

    async def to_llamaindex(self):
        from .llamaindex import get_llamaindex_tools

        await self.initialize()
        return get_llamaindex_tools(self.get_tools())

    async def to_crewai(self):
        from .crewai import get_crewai_tools

        await self.initialize()
        return get_crewai_tools(self.get_tools())

    async def to_openai(self):
        from .openai import get_openai_tools

        await self.initialize()
        return get_openai_tools(self.get_tools())

    async def to_pydantic(self):
        from .pydantic import get_pydantic_tools

        await self.initialize()
        return get_pydantic_tools(self.get_tools())

    async def to_google_adk(self):
        from .googleadk import get_google_adk_tools

        await self.initialize()
        return get_google_adk_tools(self.get_tools())

    async def to_livekit(self):
        from .livekit import get_livekit_tools

        await self.initialize()
        return get_livekit_tools(self.get_tools())

    async def connect(self, name: str):
        # Create and store the connection
        try:
            url = self._url(name)
            await self.connect_with_url(name, url)
        except Exception as e:
            if not self._fallback_url(name):
                raise e
            logger.warning(f"Error connecting to {name}: {e}\n{traceback.format_exc()}")
            url = self._fallback_url(name)
            try:
                await self.connect_with_url(name, url)
            except Exception as e:
                logger.error(f"Error connecting to {name} with fallback URL: {e}\n{traceback.format_exc()}")
                raise e

    async def connect_with_url(
        self, name: str, url: str
    ) -> None:
        """Initialize a session and load tools from it.

        Args:
            name: Name to identify this server connection
            url: The URL to connect to
        """
        logger.debug(f"Initializing session and loading tools from {url}")

        if not toolPersistances.get(name):
            logger.debug(f"Creating new persistent websocket for {name}")
            toolPersistances[name] = PersistentWebSocket(url, name, timeout=self.timeout, timeout_enabled=self.timeout_enabled)
            await toolPersistances[name].list_tools()
        logger.debug(f"Loaded {len(toolPersistances[name].get_tools())} tools from {url}")
        return toolPersistances[name].with_metas(self.metas)

    async def initialize(self) -> "BlTools":
        for i in range(0, len(self.functions), 10):
            batch = self.functions[i:i+10]
            await asyncio.gather(*(self.connect(name) for name in batch))
        return self


def bl_tools(functions: list[str], metas: dict[str, Any] = {}, timeout: int = DEFAULT_TIMEOUT, timeout_enabled: bool = True) -> BlTools:
    return BlTools(functions, metas=metas, timeout=timeout, timeout_enabled=timeout_enabled)
