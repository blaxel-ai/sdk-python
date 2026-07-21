"""Blaxel OpenAI integration module."""

try:
    from .model import *  # noqa: F403, F401
    from .tools import *  # noqa: F403, F401
except ImportError as e:
    raise ImportError(
        "The openai extra dependencies are required to use the OpenAI Agents integration. "
        "Install them with: pip install blaxel[openai]"
    ) from e
