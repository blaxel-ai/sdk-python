Module blaxel.core.mcp
======================

Sub-modules
-----------
* blaxel.core.mcp.client
* blaxel.core.mcp.server

Functions
---------

`websocket_client(url: str, headers: dict[str, typing.Any] | None = None, timeout: float = 30)`
:   Client transport for WebSocket.
    
    The `timeout` parameter controls connection timeout.

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