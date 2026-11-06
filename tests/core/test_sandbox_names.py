"""Unit tests for the sandbox naming helpers.

The control plane accepts a sandbox name only when it is lowercase letters and
digits separated by single hyphens, at most 49 characters. The SDK never renames
a sandbox on create; these helpers let callers check a name or derive one.
"""

import pytest

import blaxel.core as core
from blaxel.core.sandbox import (
    SANDBOX_NAME_MAX_LENGTH,
    is_valid_sandbox_name,
    sanitize_sandbox_name,
)
from blaxel.core.sandbox.names import _invalid_name_hint


@pytest.mark.parametrize(
    "name",
    ["a", "my-sandbox", "my-sandbox-1", "0abc", "a1-b2-c3", "x" * SANDBOX_NAME_MAX_LENGTH],
)
def test_valid_names(name):
    assert is_valid_sandbox_name(name)


@pytest.mark.parametrize(
    "name",
    [
        "",
        "sesn_01AbC",
        "My-Sandbox",
        "my_sandbox",
        "my.sandbox",
        "my sandbox",
        "-leading",
        "trailing-",
        "double--hyphen",
        "x" * (SANDBOX_NAME_MAX_LENGTH + 1),
        None,
        42,
    ],
)
def test_invalid_names(name):
    assert not is_valid_sandbox_name(name)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("sesn_01AbC", "sesn-01abc"),
        ("My Sandbox", "my-sandbox"),
        ("__a__b__", "a-b"),
        ("a.b_c d", "a-b-c-d"),
        ("already-valid", "already-valid"),
        ("UPPER", "upper"),
    ],
)
def test_sanitize(raw, expected):
    assert sanitize_sandbox_name(raw) == expected
    assert is_valid_sandbox_name(sanitize_sandbox_name(raw))


def test_sanitize_truncates_without_trailing_hyphen():
    raw = "a" * (SANDBOX_NAME_MAX_LENGTH - 1) + "_bcd"
    result = sanitize_sandbox_name(raw)
    assert result == "a" * (SANDBOX_NAME_MAX_LENGTH - 1)
    assert is_valid_sandbox_name(result)


def test_sanitize_long_id_stays_valid():
    result = sanitize_sandbox_name("Session_" + "X" * 100)
    assert len(result) == SANDBOX_NAME_MAX_LENGTH
    assert is_valid_sandbox_name(result)


@pytest.mark.parametrize("raw", ["", "___", "!!!", "-"])
def test_sanitize_rejects_names_without_letters_or_digits(raw):
    with pytest.raises(ValueError, match="no letter or digit"):
        sanitize_sandbox_name(raw)


def test_helpers_are_exported_from_blaxel_core():
    assert core.is_valid_sandbox_name is is_valid_sandbox_name
    assert core.sanitize_sandbox_name is sanitize_sandbox_name


def test_invalid_name_hint():
    assert _invalid_name_hint(None) == ""
    assert _invalid_name_hint("my-sandbox") == ""
    hint = _invalid_name_hint("sesn_01AbC")
    assert "lowercase letters, digits and single hyphens" in hint
    assert "sanitize_sandbox_name('sesn_01AbC') gives 'sesn-01abc'" in hint
    # A name with nothing to keep still gets the rule, without a suggestion.
    assert "sanitize_sandbox_name" not in _invalid_name_hint("___")
    assert "single hyphens" in _invalid_name_hint("___")
