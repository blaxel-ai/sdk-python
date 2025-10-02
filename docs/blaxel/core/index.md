Module blaxel.core
==================
Blaxel core module.

Sub-modules
-----------
* blaxel.core.agents
* blaxel.core.authentication
* blaxel.core.cache
* blaxel.core.client
* blaxel.core.common
* blaxel.core.jobs
* blaxel.core.mcp
* blaxel.core.models
* blaxel.core.sandbox
* blaxel.core.tools
* blaxel.core.volume

Functions
---------

`auth(env: str, base_url: str) ‑> blaxel.core.authentication.types.BlaxelAuth`
:   Create and return the appropriate credentials object based on available credentials.
    
    Returns:
        Credentials: The credentials object

`autoload() ‑> None`
:   

`bl_agent(name: str)`
:   

`bl_model(model_name, **kwargs)`
:   

`bl_tools(functions: list[str], metas: dict[str, typing.Any] = {}, timeout: int = 1, timeout_enabled: bool = True, transport: str = None) ‑> blaxel.core.tools.BlTools`
:   

`convert_mcp_tool_to_blaxel_tool(mcp_client: blaxel.core.tools.PersistentMcpClient, tool: mcp.types.Tool) ‑> blaxel.core.tools.types.Tool`
:   Convert an MCP tool to a blaxel tool.
    
    NOTE: this tool can be executed only in a context of an active MCP client session.
    
    Args:
        session: MCP client session
        tool: MCP tool to convert
    
    Returns:
        a LangChain tool

`find_from_cache(resource: str, name: str) ‑> typing.Any | None`
:   Find a resource from the cache by resource type and name.
    
    Args:
        resource: The resource type
        name: The resource name
    
    Returns:
        The cached resource or None if not found

`get_credentials() ‑> blaxel.core.authentication.types.CredentialsType | None`
:   Get credentials from environment variables or config file.
    
    Returns:
        CredentialsType | None: The credentials or None if not found

`websocket_client(url: str, headers: dict[str, typing.Any] | None = None, timeout: float = 30)`
:   Client transport for WebSocket.
    
    The `timeout` parameter controls connection timeout.

Classes
-------

`BLModel(model_name, **kwargs)`
:   

    ### Class variables

    `models`
    :   The type of the None singleton.

    ### Methods

    `get_parameters(self) ‑> tuple[str, str, str]`
    :

`BlAgent(name: str)`
:   

    ### Instance variables

    `external_url`
    :

    `fallback_url`
    :

    `forced_url`
    :   Get the forced URL from environment variables if set.

    `internal_url`
    :   Get the internal URL for the agent using a hash of workspace and agent name.

    `url`
    :

    ### Methods

    `acall(self, url, input_data, headers: dict = {}, params: dict = {})`
    :

    `arun(self, input: Any, headers: dict = {}, params: dict = {}) ‑> Awaitable[str]`
    :

    `call(self, url, input_data, headers: dict = {}, params: dict = {})`
    :

    `run(self, input: Any, headers: dict = {}, params: dict = {}) ‑> str`
    :

`BlJobWrapper()`
:   

    ### Instance variables

    `index: int`
    :

    `index_key: str`
    :

    ### Methods

    `get_arguments(self) ‑> Dict[str, Any]`
    :

    `start(self, func: Callable)`
    :   Run a job defined in a function, it's run in the current process.
        Handles both async and sync functions.
        Arguments are passed as keyword arguments to the function.

`BlTools(functions: list[str], metas: dict[str, typing.Any] = {}, timeout: int = 1, timeout_enabled: bool = True, transport: str = None)`
:   

    ### Methods

    `connect(self, name: str)`
    :

    `get_tools(self) ‑> list[blaxel.core.tools.types.Tool]`
    :   Get a list of all tools from all connected servers.

    `initialize(self) ‑> blaxel.core.tools.BlTools`
    :

`BlaxelAuth(credentials: blaxel.core.authentication.types.CredentialsType, workspace_name: str, base_url: str)`
:   Base class for all authentication schemes.
    
    To implement a custom authentication scheme, subclass `Auth` and override
    the `.auth_flow()` method.
    
    If the authentication scheme does I/O such as disk access or network calls, or uses
    synchronization primitives such as locks, you should override `.sync_auth_flow()`
    and/or `.async_auth_flow()` instead of `.auth_flow()` to provide specialized
    implementations that will be used by `Client` and `AsyncClient` respectively.
    
    Initializes the BlaxelAuth with the given credentials, workspace name, and base URL.
    
    Parameters:
        credentials: Credentials containing the Bearer token and refresh token.
        workspace_name (str): The name of the workspace.
        base_url (str): The base URL for authentication.

    ### Ancestors (in MRO)

    * httpx.Auth

    ### Descendants

    * blaxel.core.authentication.apikey.ApiKey
    * blaxel.core.authentication.clientcredentials.ClientCredentials
    * blaxel.core.authentication.devicemode.DeviceMode

    ### Instance variables

    `token`
    :

    ### Methods

    `get_headers(self) ‑> Dict[str, str]`
    :

`BlaxelMcpServerTransport(port: int = 8080)`
:   WebSocket server transport for MCP.
    
    Initialize the WebSocket server transport.
    
    Args:
        port: The port to listen on (defaults to 8080 or BL_SERVER_PORT env var)

    ### Methods

    `websocket_server(self)`
    :   Create and run a WebSocket server for MCP communication.

`Sandbox(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, last_used_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('SandboxSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ttl: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Micro VM for running agentic tasks
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        last_used_at (Union[Unset, str]): Last time the sandbox was used (read-only, managed by the system)
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, SandboxSpec]): Sandbox specification
        status (Union[Unset, str]): Sandbox status
        ttl (Union[Unset, int]): TTL timestamp for automatic deletion (optional, nil means no auto-deletion)
    
    Method generated by attrs for class Sandbox.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `events`
    :

    `last_used_at`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    `ttl`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SandboxFileSystem(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.action.SandboxAction

    ### Methods

    `cp(self, source: str, destination: str) ‑> blaxel.core.sandbox.types.CopyResponse`
    :

    `format_path(self, path: str) ‑> str`
    :

    `ls(self, path: str) ‑> blaxel.core.sandbox.client.models.directory.Directory`
    :

    `mkdir(self, path: str, permissions: str = '0755') ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `read(self, path: str) ‑> str`
    :

    `rm(self, path: str, recursive: bool = False) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `watch(self, path: str, callback: Callable[[blaxel.core.sandbox.types.WatchEvent], None], options: Dict[str, Any] | None = None) ‑> Dict[str, Callable]`
    :   Watch for file system changes.

    `write(self, path: str, content: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `write_binary(self, path: str, content: bytes | bytearray) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :   Write binary content to a file.

    `write_tree(self, files: List[blaxel.core.sandbox.types.SandboxFilesystemFile | Dict[str, Any]], destination_path: str | None = None) ‑> blaxel.core.sandbox.client.models.directory.Directory`
    :   Write multiple files in a tree structure.

`SandboxInstance(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxConfiguration, force_url: str | None = None, headers: Dict[str, str] | None = None, params: Dict[str, str] | None = None)`
:   

    ### Static methods

    `create(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxCreateConfiguration | Dict[str, Any] | None = None, safe: bool = True) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

    `create_if_not_exists(sandbox: blaxel.core.client.models.sandbox.Sandbox | blaxel.core.sandbox.types.SandboxCreateConfiguration | Dict[str, Any]) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Create a sandbox if it doesn't exist, otherwise return existing.

    `delete(sandbox_name: str) ‑> blaxel.core.client.models.sandbox.Sandbox`
    :

    `from_session(session: blaxel.core.sandbox.types.SessionWithToken | Dict[str, Any]) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Create a sandbox instance from a session with token.

    `get(sandbox_name: str) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

    `list() ‑> List[blaxel.core.sandbox.sandbox.SandboxInstance]`
    :

    `update_metadata(sandbox_name: str, metadata: blaxel.core.sandbox.types.SandboxUpdateMetadata) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :   Update sandbox metadata by merging new metadata with existing metadata.
        
        Args:
            sandbox_name: The name of the sandbox to update
            metadata: The metadata fields to update (labels and/or display_name)
        
        Returns:
            A new SandboxInstance with updated metadata

    ### Instance variables

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `wait(self, max_wait: int = 60000, interval: int = 1000) ‑> blaxel.core.sandbox.sandbox.SandboxInstance`
    :

`SandboxPreviews(sandbox: blaxel.core.client.models.sandbox.Sandbox)`
:   Manages sandbox previews.

    ### Instance variables

    `sandbox_name: str`
    :

    ### Methods

    `create(self, preview: blaxel.core.client.models.preview.Preview | Dict[str, Any]) ‑> blaxel.core.sandbox.preview.SandboxPreview`
    :   Create a new preview.

    `create_if_not_exists(self, preview: blaxel.core.client.models.preview.Preview | Dict[str, Any]) ‑> blaxel.core.sandbox.preview.SandboxPreview`
    :   Create a preview if it doesn't exist, otherwise return the existing one.

    `delete(self, preview_name: str) ‑> dict`
    :   Delete a preview.

    `get(self, preview_name: str) ‑> blaxel.core.sandbox.preview.SandboxPreview`
    :   Get a specific preview by name.

    `list(self) ‑> List[blaxel.core.sandbox.preview.SandboxPreview]`
    :   List all previews for the sandbox.

`SandboxProcess(sandbox_config: blaxel.core.sandbox.types.SandboxConfiguration)`
:   

    ### Ancestors (in MRO)

    * blaxel.core.sandbox.action.SandboxAction

    ### Methods

    `exec(self, process: blaxel.core.sandbox.client.models.process_request.ProcessRequest | blaxel.core.sandbox.types.ProcessRequestWithLog | Dict[str, Any]) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse | blaxel.core.sandbox.types.ProcessResponseWithLog`
    :   Execute a process in the sandbox.

    `get(self, identifier: str) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :

    `kill(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `list(self) ‑> list[blaxel.core.sandbox.client.models.process_response.ProcessResponse]`
    :

    `logs(self, identifier: str, log_type: Literal['stdout', 'stderr', 'all'] = 'all') ‑> str`
    :

    `stop(self, identifier: str) ‑> blaxel.core.sandbox.client.models.success_response.SuccessResponse`
    :

    `stream_logs(self, process_name: str, options: Dict[str, Callable[[str], None]] | None = None) ‑> Dict[str, Callable[[], None]]`
    :   Stream logs from a process with automatic reconnection and deduplication.

    `wait(self, identifier: str, max_wait: int = 60000, interval: int = 1000) ‑> blaxel.core.sandbox.client.models.process_response.ProcessResponse`
    :   Wait for a process to complete.

`VolumeCreateConfiguration(name: str | None = None, display_name: str | None = None, size: int | None = None, region: str | None = None)`
:   Simplified configuration for creating volumes with default values.

    ### Static methods

    `from_dict(data: Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeCreateConfiguration`
    :

`VolumeInstance(volume: blaxel.core.client.models.volume.Volume)`
:   

    ### Static methods

    `create(config: blaxel.core.volume.volume.VolumeCreateConfiguration | blaxel.core.client.models.volume.Volume | Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeInstance`
    :

    `create_if_not_exists(config: blaxel.core.volume.volume.VolumeCreateConfiguration | blaxel.core.client.models.volume.Volume | Dict[str, <built-in function any>]) ‑> blaxel.core.volume.volume.VolumeInstance`
    :   Create a volume if it doesn't exist, otherwise return existing.

    `delete(volume_name: str) ‑> blaxel.core.client.models.volume.Volume`
    :

    `get(volume_name: str) ‑> blaxel.core.volume.volume.VolumeInstance`
    :

    `list() ‑> list[blaxel.core.volume.volume.VolumeInstance]`
    :

    ### Instance variables

    `display_name`
    :

    `metadata`
    :

    `name`
    :

    `region`
    :

    `size`
    :

    `spec`
    :

    `status`
    :