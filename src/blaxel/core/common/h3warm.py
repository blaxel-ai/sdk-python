"""HTTP/3 (QUIC) connection warming utility.

Establishes a QUIC connection to a given hostname to pre-warm
DNS resolution and TLS 1.3/QUIC handshake, so that the first real
request benefits from a pre-warmed connection.
"""

import asyncio
import logging

from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

logger = logging.getLogger(__name__)


class H3WarmSession:
    """Holds a warmed QUIC/HTTP3 connection."""

    def __init__(self, ctx: object, client: object):
        self._ctx = ctx
        self._client = client

    def close(self) -> None:
        """Close the QUIC connection by properly exiting the async context manager."""
        try:
            if self._ctx is not None:
                loop = asyncio.new_event_loop()
                try:
                    loop.run_until_complete(self._ctx.__aexit__(None, None, None))
                finally:
                    loop.close()
                self._ctx = None
                self._client = None
        except Exception:
            pass


async def establish_h3(hostname: str, port: int = 443) -> H3WarmSession:
    """Establish an HTTP/3 (QUIC) connection to the given hostname.

    Performs DNS resolution + QUIC handshake (including TLS 1.3) to
    fully warm the connection path.

    Args:
        hostname: The SNI hostname to connect to.
        port: The port to connect to (default 443).

    Returns:
        An H3WarmSession wrapping the QUIC connection.
    """
    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=["h3"],
        server_name=hostname,
    )
    ctx = connect(hostname, port, configuration=configuration)
    client = await ctx.__aenter__()

    return H3WarmSession(ctx, client)


async def establish_h3_best_effort(hostname: str, port: int = 443) -> H3WarmSession | None:
    """Best-effort HTTP/3 warming. Returns None on any failure."""
    try:
        return await asyncio.wait_for(establish_h3(hostname, port), timeout=5.0)
    except Exception:
        return None
