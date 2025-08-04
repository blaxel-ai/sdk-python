"""Blaxel Google ADK integration module."""

import os

from .model import *  # noqa: F403, F401
from .tools import *  # noqa: F403, F401

if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "DUMMY_KEY"