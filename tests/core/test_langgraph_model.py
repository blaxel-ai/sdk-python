"""Regression tests for the langgraph token-refresh model wrapper's attribute
delegation (``TokenRefreshingWrapper.__getattr__``).

These lock in the fix for SDK-PYTHON-11Y
(``AttributeError: 'ChatAnthropic' object has no attribute '__self__'``) and the
recursion / copy hazards in the blind attribute delegation. They use a stub
wrapped model so they need neither langchain nor Blaxel credentials.
"""

import copy
import pickle

from blaxel.langgraph.model import TokenRefreshingChatModel


class _StubModel:
    """Stand-in for a wrapped chat model (e.g. ChatAnthropic).

    ``__self__`` is defined so a test can prove the wrapper does NOT delegate
    dunder lookups (delegation would return this sentinel instead of raising).
    """

    __self__ = "SHOULD_NOT_BE_DELEGATED"

    def __init__(self):
        self.model_name = "claude"

    def bind_tools(self, tools):
        # A public method the wrapper does not define itself, so reaching it
        # proves non-dunder delegation still works.
        return ("bound", tuple(tools))


class _StubChatModel(TokenRefreshingChatModel):
    """TokenRefreshingChatModel whose model creation avoids provider imports."""

    def _create_model(self):
        return _StubModel()


def _make_wrapper() -> _StubChatModel:
    return _StubChatModel(
        {"type": "anthropic", "model": "claude", "url": "http://example", "kwargs": {}}
    )


def test_dunder_self_probe_is_not_delegated():
    """SDK-PYTHON-11Y: probing ``__self__`` must not delegate to the wrapped model."""
    wrapper = _make_wrapper()

    # hasattr uses a guarded probe -- it must report False without delegating.
    assert hasattr(wrapper, "__self__") is False

    try:
        wrapper.__self__
    except AttributeError as exc:
        # The wrapper's own name, never the wrapped model's sentinel value.
        assert "__self__" in str(exc)
        assert "SHOULD_NOT_BE_DELEGATED" not in str(exc)
    else:
        raise AssertionError("expected AttributeError for wrapper.__self__")


def test_missing_attribute_before_wrapped_model_set_does_not_recurse():
    """Attribute access on a wrapper without ``wrapped_model`` must not recurse."""
    # Instances rebuilt by copy/pickle are created without __init__.
    incomplete = _StubChatModel.__new__(_StubChatModel)

    # Would raise RecursionError before the fix.
    try:
        incomplete.some_missing_attr
    except AttributeError:
        pass
    else:
        raise AssertionError("expected AttributeError, not a value")


def test_wrapped_model_access_before_set_raises_attributeerror():
    """``wrapped_model`` itself must not be delegated (it would recurse)."""
    incomplete = _StubChatModel.__new__(_StubChatModel)
    try:
        incomplete.wrapped_model
    except AttributeError as exc:
        assert "wrapped_model" in str(exc)
    else:
        raise AssertionError("expected AttributeError for wrapped_model")


def test_deepcopy_preserves_wrapper_type():
    """deepcopy must return a wrapper, not silently unwrap to the model."""
    wrapper = _make_wrapper()
    clone = copy.deepcopy(wrapper)

    assert isinstance(clone, _StubChatModel)
    assert clone is not wrapper
    assert isinstance(clone.wrapped_model, _StubModel)
    assert clone.wrapped_model is not wrapper.wrapped_model


def test_pickle_preserves_wrapper_type():
    """pickle round-trip must preserve the wrapper (dunders not delegated)."""
    wrapper = _make_wrapper()
    restored = pickle.loads(pickle.dumps(wrapper))

    assert isinstance(restored, _StubChatModel)
    assert isinstance(restored.wrapped_model, _StubModel)


def test_non_dunder_attributes_are_delegated():
    """Ordinary attribute/method delegation to the wrapped model is unchanged."""
    wrapper = _make_wrapper()

    assert wrapper.model_name == "claude"
    assert wrapper.bind_tools([1, 2]) == ("bound", (1, 2))

    try:
        wrapper.definitely_missing
    except AttributeError as exc:
        assert "definitely_missing" in str(exc)
    else:
        raise AssertionError("expected AttributeError for a missing non-dunder attr")
