
from ..client import client
from .settings import settings


def autoload() -> None:
    client.with_base_url(settings.base_url)
    client.with_auth(settings.auth)