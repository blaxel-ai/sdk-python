"""Blaxel Google ADK integration module."""

from .model import *  # noqa: F403, F401
from .tools import *  # noqa: F403, F401

import os

if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "DUMMY_KEY"