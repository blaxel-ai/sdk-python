"""Support for both mcp 1.x and mcp 2.x.

mcp 2.0 renamed FastMCP to MCPServer, made JSONRPCMessage and ClientRequest plain
unions, switched the streamable HTTP client to httpx2 and moved model attributes to
snake_case. Everything in blaxel that touches those APIs goes through this module.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import mcp.types as types
from pydantic import TypeAdapter

try:
    from mcp.server.mcpserver import MCPServer as FastMCPBase

    MCP_V2 = True
except ImportError:
    from mcp.server.fastmcp import FastMCP as FastMCPBase  # type: ignore[no-redef]

    MCP_V2 = False

if MCP_V2:
    from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client
else:
    from mcp.client.streamable_http import streamablehttp_client  # type: ignore[attr-defined]

__all__ = [
    "MCP_V2",
    "FastMCPBase",
    "call_tool_request",
    "jsonrpc_inner",
    "lowlevel_server",
    "open_streamable_http",
    "parse_jsonrpc_message",
    "tool_input_schema",
    "tool_result_is_error",
]

# In mcp 1.x JSONRPCMessage is a RootModel, in 2.x a union; a TypeAdapter parses both.
_jsonrpc_message = TypeAdapter(types.JSONRPCMessage)


def parse_jsonrpc_message(data: str | bytes) -> Any:
    """Parse one JSON-RPC message received over a transport."""
    return _jsonrpc_message.validate_json(data)


def jsonrpc_inner(message: Any) -> Any:
    """Return the concrete request/notification/response inside a JSONRPCMessage.

    mcp 1.x wraps it in a RootModel (`.root`); mcp 2.x returns it directly.
    """
    return message if MCP_V2 else getattr(message, "root", message)


def lowlevel_server(server: Any) -> Any:
    """Return the low-level mcp Server behind a FastMCP/MCPServer instance."""
    return server._lowlevel_server if MCP_V2 else server._mcp_server


def call_tool_request(params: types.CallToolRequestParams) -> Any:
    """Build a tools/call request for ClientSession.send_request."""
    request = types.CallToolRequest(method="tools/call", params=params)
    return request if MCP_V2 else types.ClientRequest(request)


def tool_input_schema(tool: types.Tool) -> dict[str, Any]:
    return tool.input_schema if MCP_V2 else tool.inputSchema  # type: ignore[attr-defined]


def tool_result_is_error(result: types.CallToolResult) -> bool:
    return bool(result.is_error if MCP_V2 else result.isError)  # type: ignore[attr-defined]


@asynccontextmanager
async def open_streamable_http(
    url: str, headers: dict[str, str] | None = None
) -> AsyncIterator[tuple[Any, Any]]:
    """Open a streamable HTTP MCP transport and yield (read_stream, write_stream)."""
    if MCP_V2:
        async with create_mcp_http_client(headers=headers) as http_client:
            async with streamable_http_client(url, http_client=http_client) as (read, write):
                yield read, write
    else:
        async with streamablehttp_client(url, headers) as (read, write, _):
            yield read, write
