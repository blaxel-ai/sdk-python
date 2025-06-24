import logging
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import urljoin, urlparse

import anyio
import mcp.types as types
from anyio.abc import TaskStatus
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp.shared.message import SessionMessage
from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect as ws_connect

logger = logging.getLogger(__name__)


def remove_request_params(url: str) -> str:
    return urljoin(url, urlparse(url).path)


@asynccontextmanager
async def websocket_client(
    url: str,
    headers: dict[str, Any] | None = None,
    timeout: float = 30,
):
    """
    Client transport for WebSocket.

    The `timeout` parameter controls connection timeout.
    """
    read_stream: MemoryObjectReceiveStream[SessionMessage | Exception]
    read_stream_writer: MemoryObjectSendStream[SessionMessage | Exception]

    write_stream: MemoryObjectSendStream[SessionMessage]
    write_stream_reader: MemoryObjectReceiveStream[SessionMessage]

    read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

    try:
        # Wrap the task group management in a try/except GeneratorExit
        try:
            async with anyio.create_task_group() as tg:
                # Convert http(s):// to ws(s)://
                ws_url = url.replace("http://", "ws://").replace("https://", "wss://")
                logger.debug(f"Connecting to WebSocket endpoint: {remove_request_params(ws_url)}")

                # Use different parameters based on websockets version
                connection_kwargs = {"additional_headers": headers, "open_timeout": timeout}

                async with ws_connect(ws_url, **connection_kwargs) as websocket:
                    logger.debug("WebSocket connection established")

                    async def ws_reader(
                        websocket: ClientConnection,
                        task_status: TaskStatus[None] = anyio.TASK_STATUS_IGNORED,
                    ):
                        try:
                            task_status.started()
                            async for message in websocket:
                                logger.debug(f"Received WebSocket message: {message}")
                                try:
                                    parsed_message = types.JSONRPCMessage.model_validate_json(
                                        message
                                    )
                                    logger.debug(f"Received server message: {parsed_message}")
                                    await read_stream_writer.send(
                                        SessionMessage(message=parsed_message)
                                    )
                                except Exception as exc:
                                    logger.error(f"Error parsing server message: {exc}")
                                    await read_stream_writer.send(exc)
                        except Exception as exc:
                            logger.error(f"Error in ws_reader: {exc}")
                            await read_stream_writer.send(exc)
                        finally:
                            await read_stream_writer.aclose()

                    async def ws_writer(websocket: ClientConnection):
                        try:
                            async with write_stream_reader:
                                async for session_message in write_stream_reader:
                                    logger.debug(
                                        f"Sending client message: {session_message.message}"
                                    )
                                    await websocket.send(
                                        session_message.message.model_dump_json(
                                            by_alias=True,
                                            exclude_none=True,
                                        )
                                    )
                                    logger.debug("Client message sent successfully")
                        except Exception as exc:
                            logger.error(f"Error in ws_writer: {exc}")
                        finally:
                            await write_stream.aclose()

                    await tg.start(ws_reader, websocket)
                    tg.start_soon(ws_writer, websocket)

                    try:
                        yield read_stream, write_stream
                    finally:
                        # Cancel tasks when the yield returns
                        tg.cancel_scope.cancel()

        except RuntimeError:
            # Context manager is exiting via GeneratorExit, this is normal.
            # Suppress it here so it doesn't get wrapped by anyio's BaseExceptionGroup.
            # The outer finally block below will still execute for cleanup.
            pass

        # The original code had the tg.cancel_scope.cancel() inside the 'finally'
        # associated with the 'yield'. Let's ensure cancellation happens
        # reliably. It seems correctly placed already.

    finally:
        # Ensure streams are closed even if task group setup fails or GeneratorExit is caught
        await read_stream_writer.aclose()
        await write_stream.aclose()
