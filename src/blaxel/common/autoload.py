
import logging

from ..client import client
from ..instrumentation.manager import telemetry_manager
from .settings import settings


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)
    telemetry_manager.initialize(settings)