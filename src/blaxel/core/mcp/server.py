import logging
import traceback
import uuid
from contextlib import asynccontextmanager
from typing import Literal

import anyio
import mcp.types as types
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp.server.fastmcp import FastMCP as FastMCPBase
from mcp.shared.message import SessionMessage
from websockets.asyncio.server import ServerConnection, serve

from ..common.env import env

logger = logging.getLogger(__name__)


class BlaxelMcpServerTransport:
    """WebSocket server transport for MCP."""

    def __init__(self, port: int = 8080):
        """Initialize the WebSocket server transport.

        Args:
            port: The port to listen on (defaults to 8080 or BL_SERVER_PORT env var)
        """
        if env["BL_SERVER_PORT"] is not None:
            self.port = int(env["BL_SERVER_PORT"])
        else:
            self.port = port
        self.clients = {}
        self.server = None

    @asynccontextmanager
    async def websocket_server(self):
        """Create and run a WebSocket server for MCP communication."""
        read_stream: MemoryObjectReceiveStream[SessionMessage | Exception]
        read_stream_writer: MemoryObjectSendStream[SessionMessage | Exception]

        write_stream: MemoryObjectSendStream[SessionMessage]
        write_stream_reader: MemoryObjectReceiveStream[SessionMessage]

        read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
        write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

        async def handler(websocket: ServerConnection):
            client_id = str(uuid.uuid4())
            self.clients[client_id] = websocket
            logger.info(f"Client connected: {client_id}")

            try:
                async for message in websocket:
                    try:
                        msg = types.JSONRPCMessage.model_validate_json(message)
                        # Modify message ID to include client ID
                        if hasattr(msg, "id") and msg.id is not None:
                            original_id = msg.id
                            msg.id = f"{client_id}:{original_id}"
                        await read_stream_writer.send(SessionMessage(message=msg))
                    except Exception as exc:
                        logger.error(f"Failed to parse message: {exc}\n{traceback.format_exc()}")
                        await read_stream_writer.send(exc)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
            finally:
                if client_id in self.clients:
                    del self.clients[client_id]
                logger.info(f"Client disconnected: {client_id}")

        async def message_sender():
            async with write_stream_reader:
                async for session_message in write_stream_reader:
                    # Extract client ID from message ID
                    client_id = None
                    msg_id = None
                    message = session_message.message
                    if hasattr(message, "id") and message.id is not None:
                        parts = str(message.id).split(":", 1)
                        if len(parts) == 2:
                            client_id, msg_id = parts
                            # Restore original message ID
                            message.id = int(msg_id) if msg_id.isdigit() else msg_id

                    data = message.model_dump_json(by_alias=True, exclude_none=True)

                    if client_id and client_id in self.clients:
                        # Send to specific client
                        websocket = self.clients[client_id]
                        try:
                            await websocket.send(data)
                        except Exception as e:
                            logger.error(f"Failed to send message to client {client_id}: {e}")
                            if client_id in self.clients:
                                del self.clients[client_id]
                    else:
                        # Broadcast to all clients
                        dead_clients = []
                        for cid, websocket in self.clients.items():
                            try:
                                await websocket.send(data)
                            except Exception:
                                dead_clients.append(cid)

                        # Clean up dead clients
                        for cid in dead_clients:
                            if cid in self.clients:
                                del self.clients[cid]

        async with anyio.create_task_group() as tg:
            logger.info(f"Starting WebSocket Server on port {self.port}")
            async with serve(handler, "0.0.0.0", self.port) as server:
                self.server = server
                tg.start_soon(message_sender)
                yield read_stream, write_stream


class FastMCP(FastMCPBase):
    def run(self, transport: Literal["stdio", "sse", "ws"] = "stdio") -> None:
        """Run the FastMCP server. Note this is a synchronous function.

        Args:
            transport: Transport protocol to use ("stdio" or "sse")
        """
        TRANSPORTS = Literal["stdio", "sse", "ws"]
        if transport not in TRANSPORTS.__args__:  # type: ignore
            raise ValueError(f"Unknown transport: {transport}")

        if transport == "stdio":
            anyio.run(self.run_stdio_async)
        elif transport == "ws":
            anyio.run(self.run_ws_async)
        else:
            anyio.run(self.run_sse_async)

    async def run_ws_async(self) -> None:
        async with BlaxelMcpServerTransport().websocket_server() as (read_stream, write_stream):
            await self._mcp_server.run(
                read_stream,
                write_stream,
                self._mcp_server.create_initialization_options(),
            )
