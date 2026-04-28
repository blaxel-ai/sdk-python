"""Tests for the Blaxel-Version header in Settings."""
import os

from blaxel.core.common.settings import BLAXEL_API_VERSION, settings


def test_default_api_version():
    """Blaxel-Version defaults to the module constant when BL_API_VERSION is unset."""
    os.environ.pop("BL_API_VERSION", None)
    assert settings.api_version == BLAXEL_API_VERSION
    assert settings.api_version == "2026-04-16"


def test_env_override_api_version():
    """BL_API_VERSION env var overrides the default."""
    os.environ["BL_API_VERSION"] = "2026-99-99"
    try:
        assert settings.api_version == "2026-99-99"
    finally:
        del os.environ["BL_API_VERSION"]


def test_headers_contain_blaxel_version():
    """headers dict includes Blaxel-Version set to the api_version value."""
    os.environ.pop("BL_API_VERSION", None)
    h = settings.headers
    assert "Blaxel-Version" in h
    assert h["Blaxel-Version"] == BLAXEL_API_VERSION
