"""Tests for hash functions."""

from blaxel.core.common.internal import get_alphanumeric_limited_hash, get_global_unique_hash


def test_get_alphanumeric_limited_hash():
    """Test alphanumeric hash generation."""
    # Test basic functionality
    result = get_alphanumeric_limited_hash("charlou-function-blaxel-search", 48)
    assert isinstance(result, str)
    assert len(result) <= 48
    assert result.isalnum()

    # Test with specific known values
    result2 = get_alphanumeric_limited_hash("main-function-explorer-mcp", 48)
    assert isinstance(result2, str)
    assert len(result2) <= 48
    assert result2.isalnum()

    # Test consistency
    result3 = get_alphanumeric_limited_hash("charlou-function-blaxel-search", 48)
    assert result == result3, "Hash should be consistent"

    # Test different max sizes
    result_short = get_alphanumeric_limited_hash("test", 10)
    assert len(result_short) <= 10


def test_get_global_unique_hash():
    """Test global unique hash generation."""
    workspace = "test-workspace"
    type_name = "function"
    name = "test-function"

    result = get_global_unique_hash(workspace, type_name, name)
    assert isinstance(result, str)
    assert len(result) <= 48
    assert result.isalnum()

    # Test consistency
    result2 = get_global_unique_hash(workspace, type_name, name)
    assert result == result2, "Global unique hash should be consistent"

    # Test different inputs produce different hashes
    result3 = get_global_unique_hash("different-workspace", type_name, name)
    assert result != result3, "Different workspaces should produce different hashes"
    # Test different inputs produce different hashes
    result3 = get_global_unique_hash("different-workspace", type_name, name)
    assert result != result3, "Different workspaces should produce different hashes"
