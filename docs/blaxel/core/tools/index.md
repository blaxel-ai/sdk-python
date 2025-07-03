Module blaxel.core.tools
========================

Sub-modules
-----------
* blaxel.core.tools.common
* blaxel.core.tools.types

Functions
---------

`bl_tools(functions: list[str], metas: dict[str, typing.Any] = {}, timeout: int = 1, timeout_enabled: bool = True) ‑> blaxel.core.tools.BlTools`
:   

`convert_mcp_tool_to_blaxel_tool(websocket_client: blaxel.core.tools.PersistentWebSocket, name: str, url: str, tool: mcp.types.Tool) ‑> blaxel.core.tools.types.Tool`
:   Convert an MCP tool to a blaxel tool.
    
    NOTE: this tool can be executed only in a context of an active MCP client session.
    
    Args:
        session: MCP client session
        tool: MCP tool to convert
    
    Returns:
        a LangChain tool

Classes
-------

`BlTools(functions: list[str], metas: dict[str, typing.Any] = {}, timeout: int = 1, timeout_enabled: bool = True)`
:   

    ### Methods

    `connect(self, name: str)`
    :

    `get_tools(self) ‑> list[blaxel.core.tools.types.Tool]`
    :   Get a list of all tools from all connected servers.

    `initialize(self) ‑> blaxel.core.tools.BlTools`
    :

`PersistentWebSocket(name: str, timeout: int = 1, timeout_enabled: bool = True)`
:   

    ### Methods

    `call_tool(self, tool_name: str, arguments: dict[str, typing.Any]) ‑> mcp.types.CallToolResult`
    :

    `get_tools(self)`
    :

    `initialize(self, fallback: bool = False)`
    :

    `list_tools(self)`
    :

    `with_metas(self, metas: dict[str, typing.Any])`
    :