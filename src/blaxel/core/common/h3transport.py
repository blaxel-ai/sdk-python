"""HTTP/3 transport for httpx via aioquic.

Provides an async H3Transport (httpx.AsyncBaseTransport) and a sync
SyncH3Transport (httpx.BaseTransport) backed by a shared connection pool
keyed by (host, port).

When UDP is blocked or an H3 connection fails mid-session, callers
automatically fall back to HTTP/2 (or HTTP/1.1 if h2 is unavailable).
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections import deque
from typing import AsyncIterator, Deque
from urllib.parse import urlparse

import httpx

try:
    from aioquic.asyncio.client import connect
    from aioquic.asyncio.protocol import QuicConnectionProtocol
    from aioquic.h3.connection import H3_ALPN, H3Connection
    from aioquic.h3.events import DataReceived, H3Event, HeadersReceived
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.quic.events import QuicEvent

    AIOQUIC_AVAILABLE = True
except ImportError:
    AIOQUIC_AVAILABLE = False

logging.getLogger("quic").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

_H3_CONNECT_TIMEOUT = 5.0
_H3_FAIL_TTL = 300.0  # remember failures for 5 min before retrying

try:
    import h2 as _h2  # noqa: F401

    HTTP2_AVAILABLE = True
except ImportError:
    HTTP2_AVAILABLE = False


# ---------------------------------------------------------------------------
# All aioquic-dependent classes are guarded so the module can be imported
# even when aioquic is not installed (optional dependency).
# ---------------------------------------------------------------------------

if AIOQUIC_AVAILABLE:

    class _H3ByteStream(httpx.AsyncByteStream):
        def __init__(self, aiterator: AsyncIterator[bytes]):
            self._aiterator = aiterator

        async def __aiter__(self) -> AsyncIterator[bytes]:
            async for part in self._aiterator:
                yield part

    class _H3Transport(QuicConnectionProtocol, httpx.AsyncBaseTransport):
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
                stream=_H3ByteStream(
                    self._receive_response_data(stream_id, stream_ended)
                ),
                extensions={"http_version": b"HTTP/3"},
            )

        # -- aioquic protocol callbacks --------------------------------------

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

        # -- internal helpers ------------------------------------------------

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

    # -----------------------------------------------------------------------
    # Sync H3 bridge (delegates to the async _H3Transport via a bg loop)
    # -----------------------------------------------------------------------

    class _SyncH3Transport(httpx.BaseTransport):
        """Sync httpx transport that delegates to an async _H3Transport."""

        def __init__(
            self, async_transport: _H3Transport, loop: asyncio.AbstractEventLoop
        ):
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

    # -----------------------------------------------------------------------
    # Fallback transports: try H3, auto-downgrade to HTTP/2 on failure
    # -----------------------------------------------------------------------

    class AsyncH3FallbackTransport(httpx.AsyncBaseTransport):
        """Async transport that tries H3 and falls back to HTTP/2 on failure."""

        def __init__(self, h3: _H3Transport, host: str, port: int):
            self._h3 = h3
            self._host = host
            self._port = port
            self._h2_fallback: httpx.AsyncHTTPTransport | None = None
            self._use_fallback = False

        async def handle_async_request(
            self, request: httpx.Request
        ) -> httpx.Response:
            if self._use_fallback:
                return await self._ensure_h2().handle_async_request(request)
            try:
                return await self._h3.handle_async_request(request)
            except Exception:
                logger.info(
                    "H3 request to %s:%d failed, downgrading to HTTP/2",
                    self._host,
                    self._port,
                )
                self._use_fallback = True
                pool._mark_failed(self._host, self._port)
                return await self._ensure_h2().handle_async_request(request)

        def _ensure_h2(self) -> httpx.AsyncHTTPTransport:
            if self._h2_fallback is None:
                self._h2_fallback = httpx.AsyncHTTPTransport(
                    http2=HTTP2_AVAILABLE
                )
            return self._h2_fallback

        async def aclose(self) -> None:
            if self._h2_fallback is not None:
                await self._h2_fallback.aclose()

    class SyncH3FallbackTransport(httpx.BaseTransport):
        """Sync transport that tries H3 and falls back to HTTP/2 on failure."""

        def __init__(self, sync_h3: _SyncH3Transport, host: str, port: int):
            self._sync_h3 = sync_h3
            self._host = host
            self._port = port
            self._h2_fallback: httpx.HTTPTransport | None = None
            self._use_fallback = False

        def handle_request(self, request: httpx.Request) -> httpx.Response:
            if self._use_fallback:
                return self._ensure_h2().handle_request(request)
            try:
                return self._sync_h3.handle_request(request)
            except Exception:
                logger.info(
                    "H3 request to %s:%d failed, downgrading to HTTP/2",
                    self._host,
                    self._port,
                )
                self._use_fallback = True
                pool._mark_failed(self._host, self._port)
                return self._ensure_h2().handle_request(request)

        def _ensure_h2(self) -> httpx.HTTPTransport:
            if self._h2_fallback is None:
                self._h2_fallback = httpx.HTTPTransport(http2=HTTP2_AVAILABLE)
            return self._h2_fallback

        def close(self) -> None:
            if self._h2_fallback is not None:
                self._h2_fallback.close()

    # -----------------------------------------------------------------------
    # Connection pool
    # -----------------------------------------------------------------------

    class H3Pool:
        """Global pool of H3 transports keyed by (host, port).

        Manages a background event loop thread for sync callers and QUIC
        connection lifecycle.  Failed hosts are remembered for
        ``_H3_FAIL_TTL`` seconds so that repeated connection attempts don't
        add latency.
        """

        def __init__(self) -> None:
            self._async_transports: dict[tuple[str, int], _H3Transport] = {}
            self._connect_contexts: dict[tuple[str, int], object] = {}
            self._failed_hosts: dict[tuple[str, int], float] = {}
            self._lock = threading.Lock()
            self._async_lock: asyncio.Lock | None = None
            self._bg_loop: asyncio.AbstractEventLoop | None = None
            self._bg_thread: threading.Thread | None = None

        def _get_async_lock(self) -> asyncio.Lock:
            if self._async_lock is None:
                self._async_lock = asyncio.Lock()
            return self._async_lock

        # -- negative cache --------------------------------------------------

        def _is_failed(self, host: str, port: int) -> bool:
            key = (host, port)
            with self._lock:
                ts = self._failed_hosts.get(key)
                if ts is None:
                    return False
                if time.monotonic() - ts > _H3_FAIL_TTL:
                    del self._failed_hosts[key]
                    return False
                return True

        def _mark_failed(self, host: str, port: int) -> None:
            key = (host, port)
            with self._lock:
                self._failed_hosts[key] = time.monotonic()
                self._connect_contexts.pop(key, None)
                self._async_transports.pop(key, None)

        # -- background event loop for sync callers --------------------------

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

                    self._bg_thread = threading.Thread(
                        target=_run_loop, daemon=True
                    )
                    self._bg_thread.start()
                    ready.wait(timeout=5)
                return self._bg_loop  # type: ignore[return-value]

        # -- internal: raw H3 connection -------------------------------------

        async def _get_or_connect(
            self, host: str, port: int
        ) -> _H3Transport | None:
            """Get a cached _H3Transport or establish a new QUIC connection."""
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
                logger.debug("H3 connection to %s:%d failed", host, port)
                self._mark_failed(host, port)
                return None

        async def _connect(self, host: str, port: int) -> _H3Transport:
            configuration = QuicConfiguration(
                is_client=True,
                alpn_protocols=H3_ALPN,
                server_name=host,
            )
            ctx = connect(
                host,
                port,
                configuration=configuration,
                create_protocol=_H3Transport,
            )
            transport = await ctx.__aenter__()
            with self._lock:
                self._connect_contexts[(host, port)] = ctx
            return transport  # type: ignore[return-value]

        # -- public async API ------------------------------------------------

        async def get_async_transport(
            self, host: str, port: int = 443
        ) -> AsyncH3FallbackTransport | None:
            """Get an H3 transport with automatic HTTP/2 fallback.

            Returns None if the QUIC handshake fails (caller should fall
            back to HTTP/2 or use ``get_async_transport_for_url`` which
            does this automatically).
            """
            if self._is_failed(host, port):
                return None
            raw = await self._get_or_connect(host, port)
            if raw is None:
                return None
            return AsyncH3FallbackTransport(raw, host, port)

        # -- public sync API (dispatches to bg loop) -------------------------

        def get_sync_transport(
            self, host: str, port: int = 443
        ) -> SyncH3FallbackTransport | None:
            """Get a sync H3 transport with automatic HTTP/2 fallback.

            Returns None on failure (caller should fall back to HTTP/2 or
            use ``get_sync_transport_for_url``).
            """
            if self._is_failed(host, port):
                return None
            loop = self._ensure_bg_loop()
            future = asyncio.run_coroutine_threadsafe(
                self._get_or_connect(host, port), loop
            )
            try:
                raw = future.result(timeout=_H3_CONNECT_TIMEOUT + 1)
            except Exception:
                self._mark_failed(host, port)
                return None
            if raw is None:
                return None
            return SyncH3FallbackTransport(
                _SyncH3Transport(raw, loop), host, port
            )

        # -- shutdown --------------------------------------------------------

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
                future = asyncio.run_coroutine_threadsafe(
                    self.close_all(), loop
                )
                try:
                    future.result(timeout=5)
                except Exception:
                    pass

    # -- module-level singleton (only when aioquic is available) -------------

    pool: H3Pool | None = H3Pool()

else:
    pool: H3Pool | None = None  # type: ignore[no-redef]


# ---------------------------------------------------------------------------
# Helpers — return the best available transport (H3 → HTTP/2 → None)
# ---------------------------------------------------------------------------


def _parse_host_port(url: str) -> tuple[str, int]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


async def get_async_transport_for_url(url: str) -> httpx.AsyncBaseTransport | None:
    """Best-effort transport for *url*: H3 with fallback, else HTTP/2, else None."""
    host, port = _parse_host_port(url)
    if not host:
        return None
    if pool is not None:
        transport = await pool.get_async_transport(host, port)
        if transport is not None:
            return transport
    if HTTP2_AVAILABLE:
        return httpx.AsyncHTTPTransport(http2=True)
    return None


def get_sync_transport_for_url(url: str) -> httpx.BaseTransport | None:
    """Best-effort transport for *url*: H3 with fallback, else HTTP/2, else None."""
    host, port = _parse_host_port(url)
    if not host:
        return None
    if pool is not None:
        transport = pool.get_sync_transport(host, port)
        if transport is not None:
            return transport
    if HTTP2_AVAILABLE:
        return httpx.HTTPTransport(http2=True)
    return None
