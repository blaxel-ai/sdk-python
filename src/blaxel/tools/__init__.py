import asyncio
import os
from contextlib import AsyncExitStack
from functools import partial
from logging import getLogger
from time import sleep
from types import TracebackType
from typing import Any, cast

from crewai.tools import BaseTool
from langchain_core.tools import StructuredTool
from llama_index.core.tools import FunctionTool
from mcp import ClientSession
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool

from ..cache import find_from_cache
from ..client import client
from ..client.api.functions import get_function
from ..client.models.function import Function
from ..common.settings import settings
from ..mcp.client import websocket_client
from .crewai import get_crewai_tools
from .langchain import get_langchain_tools
from .llamaindex import get_llamaindex_tools
from .openai import get_openai_tools
from .types import Tool

logger = getLogger(__name__)


def convert_mcp_tool_to_blaxel_tool(
    session: ClientSession,
    tool: MCPTool,
) -> Tool:
    """Convert an MCP tool to a LangChain tool.

    NOTE: this tool can be executed only in a context of an active MCP client session.

    Args:
        session: MCP client session
        tool: MCP tool to convert

    Returns:
        a LangChain tool
    """

    async def call_tool(
        *args: Any,
        **arguments: dict[str, Any],
    ) -> CallToolResult:
        logger.debug(f"Calling tool {tool.name} with arguments {arguments}")
        call_tool_result = await session.call_tool(tool.name, arguments)
        logger.debug(f"Tool {tool.name} returned {call_tool_result}")
        return call_tool_result

    def sync_call_tool(**arguments: dict[str, Any]) -> CallToolResult:
        try:
            loop = asyncio.get_running_loop()
            return loop.run_until_complete(session.call_tool(tool.name, arguments))
        except RuntimeError:
            return asyncio.run(session.call_tool(tool.name, arguments))

    return Tool(
        name=tool.name,
        description=tool.description or "",
        input_schema=tool.inputSchema,
        coroutine=call_tool,
        sync_coroutine=sync_call_tool,
        response_format="content_and_artifact",
    )


async def load_mcp_tools(session: ClientSession) -> list[Tool]:
    """Load all available MCP tools and convert them to LangChain tools."""
    tools = await session.list_tools()
    return [convert_mcp_tool_to_blaxel_tool(session, tool) for tool in tools.tools]

class BlTools:
    def __init__(self, functions: list[str]):
        self.exit_stack = AsyncExitStack()
        self.sessions: dict[str, ClientSession] = {}
        self.server_name_to_tools: dict[str, list[Tool]] = {}
        self.functions = functions

    def _external_url(self, name: str) -> str:
        return f"{settings.run_url}/{settings.auth.workspace_name}/functions/{name}"

    def _url(self, name: str) -> str:
        env_var = name.replace("-", "_").upper()
        if os.getenv(f"BL_FUNCTION_{env_var}_URL"):
            return os.getenv(f"BL_FUNCTION_{env_var}_URL")
        elif os.getenv(f"BL_FUNCTION_{env_var}_SERVICE_NAME"):
            return f"https://{os.getenv(f'BL_FUNCTION_{env_var}_SERVICE_NAME')}.{settings.run_internal_hostname}"
        return self._external_url(name)

    def _fallback_url(self, name: str) -> str | None:
        if self._external_url(name) != self._url(name):
            return self._external_url(name)
        return None

    def get_tools(self) -> list[Tool]:
        """Get a list of all tools from all connected servers."""
        all_tools: list[Tool] = []
        for server_tools in self.server_name_to_tools.values():
            all_tools.extend(server_tools)
        return all_tools

    def to_langchain(self) -> list[StructuredTool]:
        return get_langchain_tools(self.get_tools())

    def to_llamaindex(self) -> list[FunctionTool]:
        return get_llamaindex_tools(self.get_tools())

    def to_crewai(self) -> list[BaseTool]:
        return get_crewai_tools(self.get_tools())

    def to_openai(self) -> list[FunctionTool]:
        return get_openai_tools(self.get_tools())

    async def connect_to_server_via_websocket(self, name: str):
        # Create and store the connection
        try:
            url = self._url(name)
            headers = settings.auth.get_headers()
            read, write = await self.exit_stack.enter_async_context(websocket_client(url, headers, timeout=30))
            session = cast(
                ClientSession,
                await self.exit_stack.enter_async_context(ClientSession(read, write)),
            )
            await self._initialize_session_and_load_tools(name, session)
        except Exception as e:
            if not self._fallback_url(name):
                raise e
            url = self._fallback_url(name)
            headers = settings.auth.get_headers()
            read, write = await self.exit_stack.enter_async_context(websocket_client(url, headers))
            session = cast(
                ClientSession,
                await self.exit_stack.enter_async_context(ClientSession(read, write)),
            )
            await self._initialize_session_and_load_tools(name, session)

    async def _initialize_session_and_load_tools(
        self, name: str, session: ClientSession
    ) -> None:
        """Initialize a session and load tools from it.

        Args:
            server_name: Name to identify this server connection
            session: The ClientSession to initialize
        """
        # Initialize the session
        await session.initialize()
        self.sessions[name] = session

        # Load tools from this server
        server_tools = await load_mcp_tools(session)
        self.server_name_to_tools[name] = server_tools

    async def _get_function(self, tool) -> Function | None:
        cache_data = await find_from_cache('Function', tool)
        if cache_data:
            return Function(**cache_data)
        try:
            return await get_function.asyncio(client=client, function_name=tool)
        except Exception as e:
            return None

    async def __aenter__(self) -> "BlTools":
        try:
            functions = []
            for name in self.functions:
                function = await self._get_function(name)
                if function:
                    functions.append(function)
                else:
                    if not os.getenv(f"BL_FUNCTION_{name.replace('-', '_').upper()}_URL"):
                        logger.warning(f"Function {name} not loaded, skipping")
                await self.connect_to_server_via_websocket(name)
            return self
        except Exception:
            await self.exit_stack.aclose()
            raise

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.exit_stack.aclose()

def bl_tools(functions: list[str]) -> BlTools:
    return BlTools(functions)
