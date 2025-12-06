"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

__version__ = ""
__commit__ = ""
__sentry_dsn__ = ""
__all__ = ["autoload", "settings", "env"]

autoload()
