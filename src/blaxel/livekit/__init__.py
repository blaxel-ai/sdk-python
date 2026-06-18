"""Blaxel LiveKit integration module."""

try:
    from .model import *  # noqa: F403, F401
    from .tools import *  # noqa: F403, F401
except ImportError as e:
    raise ImportError(
        "The livekit extra dependencies are required to use the LiveKit integration. "
        "Install them with: pip install blaxel[livekit]"
    ) from e
