"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

autoload()

__version__ = "0.2.0"
__all__ = ["autoload", "settings", "env"]
