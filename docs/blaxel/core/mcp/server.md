Module blaxel.core.mcp.server
=============================

Classes
-------

`BlaxelMcpServerTransport(port: int = 8080)`
:   WebSocket server transport for MCP.
    
    Initialize the WebSocket server transport.
    
    Args:
        port: The port to listen on (defaults to 8080 or BL_SERVER_PORT env var)

    ### Class variables

    `spans: Dict[str, opentelemetry.trace.span.Span]`
    :

    ### Methods

    `websocket_server(self)`
    :   Create and run a WebSocket server for MCP communication.

`FastMCP(name: str | None = None, instructions: str | None = None, auth_server_provider: OAuthAuthorizationServerProvider[Any, Any, Any] | None = None, **settings: Any)`
:   

    ### Ancestors (in MRO)

    * mcp.server.fastmcp.server.FastMCP

    ### Methods

    `run(self, transport: Literal['stdio', 'sse', 'ws'] = 'stdio') ‑> None`
    :   Run the FastMCP server. Note this is a synchronous function.
        
        Args:
            transport: Transport protocol to use ("stdio" or "sse")

    `run_ws_async(self) ‑> None`
    :