import logging

from ..client import client
from .settings import settings

logger = logging.getLogger(__name__)


def telemetry() -> None:
    from blaxel.telemetry import telemetry_manager

    telemetry_manager.initialize(settings)


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)
    try:
        telemetry()
    except Exception:
        pass
