"""HTTP/3 transport for httpx via aioquic.

Provides an async H3Transport (httpx.AsyncBaseTransport) and a sync
SyncH3Transport (httpx.BaseTransport) backed by a shared connection pool
keyed by (host, port).
"""

from __future__ import annotations

import asyncio
import logging
import socket
import threading
from collections import deque
from typing import AsyncIterator, Deque
from urllib.parse import urlparse

import httpx
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import DataReceived, H3Event, HeadersReceived
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent

logging.getLogger("quic").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

_H3_CONNECT_TIMEOUT = 5.0


# ---------------------------------------------------------------------------
# Async H3 transport (one QUIC connection per instance)
# ---------------------------------------------------------------------------

class _H3ByteStream(httpx.AsyncByteStream):
    def __init__(self, aiterator: AsyncIterator[bytes]):
        self._aiterator = aiterator

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for part in self._aiterator:
            yield part


class H3Transport(QuicConnectionProtocol, httpx.AsyncBaseTransport):
    """httpx async transport over a single QUIC/H3 connection."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)
        self._read_queue: dict[int, Deque[H3Event]] = {}
        self._read_ready: dict[int, asyncio.Event] = {}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        assert isinstance(request.stream, httpx.AsyncByteStream)

        stream_id = self._quic.get_next_available_stream_id()
        self._read_queue[stream_id] = deque()
        self._read_ready[stream_id] = asyncio.Event()

        self._http.send_headers(
            stream_id=stream_id,
            headers=[
                (b":method", request.method.encode()),
                (b":scheme", request.url.raw_scheme),
                (b":authority", request.url.netloc),
                (b":path", request.url.raw_path),
            ]
            + [
                (k.lower(), v)
                for (k, v) in request.headers.raw
                if k.lower() not in (b"connection", b"host")
            ],
        )
        async for data in request.stream:
            self._http.send_data(stream_id=stream_id, data=data, end_stream=False)
        self._http.send_data(stream_id=stream_id, data=b"", end_stream=True)
        self.transmit()

        status_code, headers, stream_ended = await self._receive_response(stream_id)

        return httpx.Response(
            status_code=status_code,
            headers=headers,
            stream=_H3ByteStream(self._receive_response_data(stream_id, stream_ended)),
            extensions={"http_version": b"HTTP/3"},
        )

    # -- aioquic protocol callbacks ------------------------------------------

    def http_event_received(self, event: H3Event) -> None:
        if isinstance(event, (HeadersReceived, DataReceived)):
            stream_id = event.stream_id
            if stream_id in self._read_queue:
                self._read_queue[stream_id].append(event)
                self._read_ready[stream_id].set()

    def quic_event_received(self, event: QuicEvent) -> None:
        if self._http is not None:
            for http_event in self._http.handle_event(event):
                self.http_event_received(http_event)

    # -- internal helpers ----------------------------------------------------

    async def _receive_response(self, stream_id: int):
        stream_ended = False
        while True:
            event = await self._wait_for_http_event(stream_id)
            if isinstance(event, HeadersReceived):
                stream_ended = event.stream_ended
                break

        headers = []
        status_code = 0
        for header, value in event.headers:
            if header == b":status":
                status_code = int(value.decode())
            else:
                headers.append((header, value))
        return status_code, headers, stream_ended

    async def _receive_response_data(
        self, stream_id: int, stream_ended: bool
    ) -> AsyncIterator[bytes]:
        while not stream_ended:
            event = await self._wait_for_http_event(stream_id)
            if isinstance(event, DataReceived):
                stream_ended = event.stream_ended
                yield event.data
            elif isinstance(event, HeadersReceived):
                stream_ended = event.stream_ended

    async def _wait_for_http_event(self, stream_id: int) -> H3Event:
        if not self._read_queue[stream_id]:
            await self._read_ready[stream_id].wait()
        event = self._read_queue[stream_id].popleft()
        if not self._read_queue[stream_id]:
            self._read_ready[stream_id].clear()
        return event


# ---------------------------------------------------------------------------
# Sync H3 transport (bridges async transport via a background event loop)
# ---------------------------------------------------------------------------

class SyncH3Transport(httpx.BaseTransport):
    """Sync httpx transport that delegates to an async H3Transport."""

    def __init__(self, async_transport: H3Transport, loop: asyncio.AbstractEventLoop):
        self._async_transport = async_transport
        self._loop = loop

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        future = asyncio.run_coroutine_threadsafe(
            self._async_transport.handle_async_request(request),
            self._loop,
        )
        return future.result(timeout=300)

    def close(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Connection pool
# ---------------------------------------------------------------------------

class H3Pool:
    """Global pool of H3 transports keyed by (host, port).

    Manages a background event loop thread for sync callers and QUIC
    connection lifecycle.
    """

    def __init__(self) -> None:
        self._async_transports: dict[tuple[str, int], H3Transport] = {}
        self._connect_contexts: dict[tuple[str, int], object] = {}
        self._lock = threading.Lock()
        self._async_lock: asyncio.Lock | None = None
        self._bg_loop: asyncio.AbstractEventLoop | None = None
        self._bg_thread: threading.Thread | None = None

    def _get_async_lock(self) -> asyncio.Lock:
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        return self._async_lock

    # -- background event loop for sync callers ------------------------------

    def _ensure_bg_loop(self) -> asyncio.AbstractEventLoop:
        with self._lock:
            if self._bg_loop is None or not self._bg_loop.is_running():
                ready = threading.Event()

                def _run_loop():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    self._bg_loop = loop
                    ready.set()
                    loop.run_forever()

                self._bg_thread = threading.Thread(target=_run_loop, daemon=True)
                self._bg_thread.start()
                ready.wait(timeout=5)
            return self._bg_loop  # type: ignore[return-value]

    # -- async API -----------------------------------------------------------

    async def get_async_transport(
        self, host: str, port: int = 443
    ) -> H3Transport | None:
        """Get or create an H3Transport for the given host.

        Returns None if the QUIC handshake fails (caller should fall back
        to TCP).
        """
        key = (host, port)
        async with self._get_async_lock():
            transport = self._async_transports.get(key)
            if transport is not None:
                return transport
        try:
            transport = await asyncio.wait_for(
                self._connect(host, port), timeout=_H3_CONNECT_TIMEOUT
            )
            async with self._get_async_lock():
                self._async_transports[key] = transport
            return transport
        except Exception:
            logger.debug("H3 connection to %s:%d failed, falling back to TCP", host, port)
            return None

    async def _connect(self, host: str, port: int) -> H3Transport:
        configuration = QuicConfiguration(
            is_client=True,
            alpn_protocols=H3_ALPN,
            server_name=host,
        )
        ctx = connect(
            host,
            port,
            configuration=configuration,
            create_protocol=H3Transport,
        )
        transport = await ctx.__aenter__()
        with self._lock:
            self._connect_contexts[(host, port)] = ctx
        return transport  # type: ignore[return-value]

    # -- sync API (dispatches to bg loop) ------------------------------------

    def get_sync_transport(
        self, host: str, port: int = 443
    ) -> SyncH3Transport | None:
        """Get or create a SyncH3Transport for the given host.

        Returns None on failure (caller should fall back to TCP).
        """
        loop = self._ensure_bg_loop()
        future = asyncio.run_coroutine_threadsafe(
            self.get_async_transport(host, port), loop
        )
        try:
            async_transport = future.result(timeout=_H3_CONNECT_TIMEOUT + 1)
        except Exception:
            return None
        if async_transport is None:
            return None
        return SyncH3Transport(async_transport, loop)

    # -- shutdown ------------------------------------------------------------

    async def close_all(self) -> None:
        async with self._get_async_lock():
            for key, ctx in list(self._connect_contexts.items()):
                try:
                    await ctx.__aexit__(None, None, None)
                except Exception:
                    pass
            self._async_transports.clear()
            self._connect_contexts.clear()

    def close_all_sync(self) -> None:
        loop = self._bg_loop
        if loop is not None and loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.close_all(), loop)
            try:
                future.result(timeout=5)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

pool = H3Pool()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_host_port(url: str) -> tuple[str, int]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


async def get_async_transport_for_url(url: str) -> H3Transport | None:
    host, port = _parse_host_port(url)
    if not host:
        return None
    return await pool.get_async_transport(host, port)


def get_sync_transport_for_url(url: str) -> SyncH3Transport | None:
    host, port = _parse_host_port(url)
    if not host:
        return None
    return pool.get_sync_transport(host, port)
