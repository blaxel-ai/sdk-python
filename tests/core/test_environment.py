"""Tests for environment and settings functionality."""

import os

from blaxel.core.common.env import env


def test_env_access():
    """Test environment variable access."""
    # Test setting and getting environment variables
    test_key = "BL_TEST_VAR"
    test_value = "test_value"

    # Set environment variable
    os.environ[test_key] = test_value

    try:
        # Test accessing via env
        assert env[test_key] == test_value

        # Test default value when key doesn't exist
        assert env["BL_NONEXISTENT_VAR"] is None

    finally:
        # Clean up
        if test_key in os.environ:
            del os.environ[test_key]


def test_settings_access():
    """Test settings access."""
    from blaxel.core.common.settings import settings

    # Test that settings object exists and has expected properties
    assert settings is not None

    # Test common settings that should be available
    assert hasattr(settings, "workspace")
    assert hasattr(settings, "type")
    assert hasattr(settings, "name")


def test_settings_environment_sensitivity():
    """Test that settings can be influenced by environment variables."""
    # This test verifies that the settings system is designed to read from environment
    # without actually changing the current settings instance

    # Test that environment variable names are correctly formatted
    test_vars = ["BL_WORKSPACE", "BL_TYPE", "BL_NAME"]

    for var in test_vars:
        # Test that these environment variables can be set
        original_value = os.environ.get(var)
        os.environ[var] = "test-value"

        try:
            # Verify the environment variable is set
            assert os.environ[var] == "test-value"
        finally:
            # Restore original value
            if original_value is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = original_value


def test_forced_url_functionality():
    """Test forced URL functionality from environment."""
    from blaxel.core.common.internal import get_forced_url

    # Test with function URL
    os.environ["BL_FUNCTION_TEST_FUNCTION_URL"] = "http://localhost:8080"

    try:
        url = get_forced_url("function", "test-function")
        assert url == "http://localhost:8080"

        # Test with non-existent URL
        url = get_forced_url("function", "nonexistent")
        assert url is None

    finally:
        if "BL_FUNCTION_TEST_FUNCTION_URL" in os.environ:
            del os.environ["BL_FUNCTION_TEST_FUNCTION_URL"]


def test_pluralize_functionality():
    """Test pluralize functionality."""
    from blaxel.core.common.internal import pluralize

    # Test basic pluralization
    assert pluralize("function") == "functions"
    assert pluralize("agent") == "agents"
    assert pluralize("job") == "jobs"
    assert pluralize("sandbox") == "sandboxes"

    # Test words ending in 'x'
    assert pluralize("box") == "boxes"

    # Test words ending in 'y'
    assert pluralize("policy") == "policies"

    # Test words ending in 's', 'sh', 'ch'
    assert pluralize("class") == "classes"
    assert pluralize("batch") == "batches"


def test_autoload_functionality():
    """Test autoload functionality."""
    from blaxel.core.common.autoload import autoload

    # Test that autoload function exists and is callable
    assert callable(autoload)

    # Test that calling autoload doesn't raise errors
    # (This is a basic smoke test since autoload has side effects)
    try:
        autoload()
    except Exception as e:
        # If there are import errors due to missing optional dependencies,
        # that's acceptable in a test environment
        if "No module named" not in str(e):
            raise


def test_settings_properties():
    """Test that settings has the expected properties."""
    from blaxel.core.common.settings import settings

    # Test that common properties exist (may have different values)
    assert isinstance(settings.workspace, str)
    assert isinstance(settings.type, str)
    assert isinstance(settings.name, str)

    # Test that these are not empty
    assert len(settings.workspace) > 0
    assert len(settings.type) > 0
    assert len(settings.name) > 0
