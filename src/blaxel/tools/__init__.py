import asyncio
import json
from contextlib import AsyncExitStack
from logging import getLogger
from typing import Any, cast

from mcp import ClientSession
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool

from ..client.models import Function
from ..common.env import env
from ..common.settings import settings
from ..instrumentation.span import SpanManager
from ..mcp.client import websocket_client
from .types import Tool
import traceback

logger = getLogger(__name__)

class PersistentWebSocket:
    def __init__(self, url: str, timeout: int = 5):
        self.url = url
        self.timeout = timeout
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession = None
        self.timer_task = None

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> CallToolResult:
        await self._initialize()
        self._remove_timer()
        logger.debug(f"Calling tool {tool_name} with arguments {arguments}")
        call_tool_result = await self.session.call_tool(tool_name, arguments)
        logger.debug(f"Tool {tool_name} returned {call_tool_result}")
        self._reset_timer()
        return call_tool_result
    
    async def list_tools(self):
        await self._initialize()
        self._remove_timer()
        logger.debug("Listing tools")
        list_tools_result = await self.session.list_tools()
        logger.debug(f"Tools listed: {list_tools_result}")
        self._reset_timer()
        return list_tools_result

    async def _initialize(self):
        if not self.session:
            logger.debug(f"Initializing websocket client for {self.url}")
            read, write = await self.exit_stack.enter_async_context(websocket_client(self.url, settings.headers))
            self.session = cast(ClientSession, await self.exit_stack.enter_async_context(ClientSession(read, write)))
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
            await self.exit_stack.aclose()
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
        }
        with SpanManager("blaxel-tracer").create_active_span("blaxel-tool-call", span_attributes) as span:
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


class BlTools:
    tools_by_server: dict[str, list[Tool]] = {}

    def __init__(self, functions: list[str]):
        self.exit_stack = AsyncExitStack()
        self.sessions: dict[str, ClientSession] = {}
        self.functions = functions

    def _external_url(self, name: str) -> str:
        return f"{settings.run_url}/{settings.auth.workspace_name}/functions/{name}"

    def _url(self, name: str) -> str:
        env_var = name.replace("-", "_").upper()
        if env[f"BL_FUNCTION_{env_var}_URL"]:
            return env[f"BL_FUNCTION_{env_var}_URL"]
        elif env[f"BL_FUNCTION_{env_var}_SERVICE_NAME"]:
            return f"https://{env[f'BL_FUNCTION_{env_var}_SERVICE_NAME']}.{settings.run_internal_hostname}"
        return self._external_url(name)

    def _fallback_url(self, name: str) -> str | None:
        if self._external_url(name) != self._url(name):
            return self._external_url(name)
        return None

    def get_tools(self) -> list[Tool]:
        """Get a list of all tools from all connected servers."""
        all_tools: list[Tool] = []
        for server_tools in BlTools.tools_by_server.values():
            all_tools.extend(server_tools)
        return all_tools

    async def to_langchain(self):
        from .langchain import get_langchain_tools

        await self.intialize()
        return get_langchain_tools(self.get_tools())

    async def to_llamaindex(self):
        from .llamaindex import get_llamaindex_tools

        await self.intialize()
        return get_llamaindex_tools(self.get_tools())

    async def to_crewai(self):
        from .crewai import get_crewai_tools

        await self.intialize()
        return get_crewai_tools(self.get_tools())

    async def to_openai(self):
        from .openai import get_openai_tools

        await self.intialize()
        return get_openai_tools(self.get_tools())

    async def connect_to_server_via_websocket(self, name: str):
        # Create and store the connection
        try:
            url = self._url(name)
            await self._initialize_session_and_load_tools(name, url)
        except Exception as e:
            if not self._fallback_url(name):
                raise e
            url = self._fallback_url(name)
            await self._initialize_session_and_load_tools(name, url)

    async def _initialize_session_and_load_tools(
        self, name: str, url: str
    ) -> None:
        """Initialize a session and load tools from it.

        Args:
            name: Name to identify this server connection
            url: The URL to connect to
        """
        logger.debug(f"Initializing session and loading tools from {url}")
        if not BlTools.tools_by_server.get(name):
            BlTools.tools_by_server[name] = await self.load_mcp_tools(name, url)
        logger.debug(f"Loaded {len(BlTools.tools_by_server[name])} tools from {url}")

    async def load_mcp_tools(self, name: str, url: str) -> list[Tool]:
        """Load all available MCP tools and convert them to Blaxel tools."""
        websocket = PersistentWebSocket(url)
        tools = await websocket.list_tools()
        return [convert_mcp_tool_to_blaxel_tool(websocket, name, url, tool) for tool in tools.tools]

    async def initialize_function(self, name: str) -> Function | None:
        try:
            await self.connect_to_server_via_websocket(name)
        except Exception as e:
            logger.warning(f"Failed to connect to server {name}: {e}: {traceback.format_exc()}")
            return None
    async def intialize(self) -> "BlTools":
        try:
            # Process functions in batches of 10 concurrently
            for i in range(0, len(self.functions), 10):
                batch = self.functions[i:i+10]
                await asyncio.gather(*(self.initialize_function(name) for name in batch))
            return self
        except Exception:
            await self.exit_stack.aclose()
            raise


def bl_tools(functions: list[str]) -> BlTools:
    return BlTools(functions)
