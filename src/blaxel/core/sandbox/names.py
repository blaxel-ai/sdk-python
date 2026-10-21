"""Sandbox naming rule, and helpers to check a name or derive a valid one.

The control plane rejects a sandbox name with a 400 unless it is made of
lowercase letters and digits, optionally separated by single hyphens, with no
leading or trailing hyphen, and at most ``SANDBOX_NAME_MAX_LENGTH`` characters.
"""

import re

SANDBOX_NAME_MAX_LENGTH = 49

_VALID_SANDBOX_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_INVALID_CHARACTERS = re.compile(r"[^a-z0-9]+")


def is_valid_sandbox_name(name: str) -> bool:
    """Return True when the control plane accepts ``name`` as a sandbox name.

    Valid names use lowercase letters, digits and single hyphens between them
    (``my-sandbox-1``), and are at most ``SANDBOX_NAME_MAX_LENGTH`` characters.
    Uppercase letters, underscores, dots, spaces and leading, trailing or
    doubled hyphens are rejected.
    """
    return (
        isinstance(name, str)
        and len(name) <= SANDBOX_NAME_MAX_LENGTH
        and _VALID_SANDBOX_NAME.fullmatch(name) is not None
    )


def sanitize_sandbox_name(name: str) -> str:
    """Derive a valid sandbox name from any string, such as an external id.

    Lowercases ``name``, replaces each run of other characters (underscores,
    dots, spaces, ...) with one hyphen, trims hyphens at both ends and cuts the
    result to ``SANDBOX_NAME_MAX_LENGTH`` characters. A valid name is returned
    unchanged, so ``sanitize_sandbox_name("sesn_01AbC")`` gives ``"sesn-01abc"``.

    The mapping is lossy: ids that differ only by case or punctuation give the
    same name. Keep the original id yourself (for example in a label) if you
    need to map back to it.

    Raises:
        ValueError: when ``name`` has no letter or digit to build a name from.
    """
    sanitized = _INVALID_CHARACTERS.sub("-", name.lower()).strip("-")
    sanitized = sanitized[:SANDBOX_NAME_MAX_LENGTH].rstrip("-")
    if not sanitized:
        raise ValueError(f"Cannot derive a sandbox name from {name!r}: it has no letter or digit.")
    return sanitized


def _invalid_name_hint(name: str | None) -> str:
    """Hint appended to a rejected creation when the requested name breaks the rule."""
    if not name or is_valid_sandbox_name(name):
        return ""
    hint = (
        " Sandbox names use lowercase letters, digits and single hyphens"
        f" (at most {SANDBOX_NAME_MAX_LENGTH} characters)."
    )
    try:
        return f"{hint} sanitize_sandbox_name({name!r}) gives {sanitize_sandbox_name(name)!r}."
    except ValueError:
        return hint
