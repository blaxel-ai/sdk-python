Module blaxel.core.mcp.server
=============================

Classes
-------

`BlaxelMcpServerTransport(port: int = 8080)`
:   WebSocket server transport for MCP.
    
    Initialize the WebSocket server transport.
    
    Args:
        port: The port to listen on (defaults to 8080 or BL_SERVER_PORT env var)

    ### Methods

    `websocket_server(self)`
    :   Create and run a WebSocket server for MCP communication.

`FastMCP(name: str | None = None, instructions: str | None = None, auth_server_provider: OAuthAuthorizationServerProvider[Any, Any, Any] | None = None, token_verifier: TokenVerifier | None = None, event_store: EventStore | None = None, *, tools: list[Tool] | None = None, debug: bool = False, log_level: "Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']" = 'INFO', host: str = '127.0.0.1', port: int = 8000, mount_path: str = '/', sse_path: str = '/sse', message_path: str = '/messages/', streamable_http_path: str = '/mcp', json_response: bool = False, stateless_http: bool = False, warn_on_duplicate_resources: bool = True, warn_on_duplicate_tools: bool = True, warn_on_duplicate_prompts: bool = True, dependencies: Collection[str] = (), lifespan: Callable[[FastMCP[LifespanResultT]], AbstractAsyncContextManager[LifespanResultT]] | None = None, auth: AuthSettings | None = None, transport_security: TransportSecuritySettings | None = None)`
:   Abstract base class for generic types.
    
    On Python 3.12 and newer, generic classes implicitly inherit from
    Generic when they declare a parameter list after the class's name::
    
        class Mapping[KT, VT]:
            def __getitem__(self, key: KT) -> VT:
                ...
            # Etc.
    
    On older versions of Python, however, generic classes have to
    explicitly inherit from Generic.
    
    After a class has been declared to be generic, it can then be used as
    follows::
    
        def lookup_name[KT, VT](mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
            try:
                return mapping[key]
            except KeyError:
                return default

    ### Ancestors (in MRO)

    * mcp.server.fastmcp.server.FastMCP
    * typing.Generic

    ### Methods

    `run(self, transport: Literal['stdio', 'sse', 'ws'] = 'stdio') ‑> None`
    :   Run the FastMCP server. Note this is a synchronous function.
        
        Args:
            transport: Transport protocol to use ("stdio" or "sse")

    `run_ws_async(self) ‑> None`
    :