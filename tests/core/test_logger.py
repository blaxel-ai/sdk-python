import io
import logging

import pytest

from blaxel.core.common.logger import (
    PROVIDER_DEBUG_LOGGER_NAMES,
    suppress_provider_debug_loggers,
)


@pytest.fixture
def restore_provider_loggers():
    tracked = {}
    for name in PROVIDER_DEBUG_LOGGER_NAMES:
        logger = logging.getLogger(name)
        tracked[name] = {
            "level": logger.level,
            "propagate": logger.propagate,
            "handlers": list(logger.handlers),
            "handler_levels": {handler: handler.level for handler in logger.handlers},
        }

    yield

    for name, state in tracked.items():
        logger = logging.getLogger(name)
        for handler in list(logger.handlers):
            if handler not in state["handlers"]:
                logger.removeHandler(handler)
                handler.close()
        logger.handlers[:] = state["handlers"]
        for handler, level in state["handler_levels"].items():
            handler.setLevel(level)
        logger.setLevel(state["level"])
        logger.propagate = state["propagate"]


def test_suppresses_high_risk_provider_loggers_by_default(monkeypatch, restore_provider_loggers):
    monkeypatch.delenv("BL_ALLOW_PROVIDER_DEBUG_LOGS", raising=False)

    for logger_name in PROVIDER_DEBUG_LOGGER_NAMES:
        logger = logging.getLogger(logger_name)
        handler = logging.StreamHandler(io.StringIO())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    suppress_provider_debug_loggers()

    for logger_name in PROVIDER_DEBUG_LOGGER_NAMES:
        logger = logging.getLogger(logger_name)
        assert logger.getEffectiveLevel() >= logging.WARNING
        assert all(handler.level >= logging.WARNING for handler in logger.handlers)


def test_provider_debug_payload_patterns_do_not_emit_by_default(
    monkeypatch, restore_provider_loggers
):
    monkeypatch.delenv("BL_ALLOW_PROVIDER_DEBUG_LOGS", raising=False)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger("LiteLLM")
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    suppress_provider_debug_loggers()
    logger.debug(
        "X-Blaxel-Authorization: Bearer "
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature "
        "Request options LLM Request RAW RESPONSE"
    )

    assert stream.getvalue() == ""


def test_provider_debug_opt_in_preserves_debug_behavior(monkeypatch, restore_provider_loggers):
    monkeypatch.setenv("BL_ALLOW_PROVIDER_DEBUG_LOGS", "true")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger("LiteLLM")
    logger.addHandler(handler)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    suppress_provider_debug_loggers()
    logger.debug("visible provider debug")

    assert logger.getEffectiveLevel() == logging.DEBUG
    assert handler.level == logging.DEBUG
    assert "visible provider debug" in stream.getvalue()
