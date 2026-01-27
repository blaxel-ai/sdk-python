"""Tests for WatchHandle, AsyncWatchHandle, StreamHandle, and AsyncStreamHandle classes."""

import pytest

from blaxel.core.sandbox import (
    AsyncStreamHandle,
    AsyncWatchHandle,
    StreamHandle,
    WatchHandle,
)


class TestWatchHandle:
    """Tests for WatchHandle (sync version)."""

    def test_close_calls_close_func(self):
        """Test that close() calls the close function."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = WatchHandle(close_func)
        assert not close_called
        handle.close()
        assert close_called

    def test_close_only_calls_once(self):
        """Test that close() only calls the function once."""
        call_count = 0

        def close_func():
            nonlocal call_count
            call_count += 1

        handle = WatchHandle(close_func)
        handle.close()
        handle.close()
        handle.close()
        assert call_count == 1

    def test_closed_property(self):
        """Test the closed property."""
        handle = WatchHandle(lambda: None)
        assert not handle.closed
        handle.close()
        assert handle.closed

    def test_context_manager(self):
        """Test using WatchHandle as a context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with WatchHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    def test_context_manager_on_exception(self):
        """Test that context manager closes on exception."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with pytest.raises(ValueError):
            with WatchHandle(close_func):
                raise ValueError("Test error")

        assert close_called

    def test_dict_like_access_backward_compatibility(self):
        """Test backward compatibility with dict-like access."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = WatchHandle(close_func)
        # Should support handle["close"]() for backward compatibility
        handle["close"]()
        assert close_called

    def test_dict_like_access_invalid_key(self):
        """Test that invalid key raises KeyError."""
        handle = WatchHandle(lambda: None)
        with pytest.raises(KeyError):
            handle["invalid_key"]


class TestAsyncWatchHandle:
    """Tests for AsyncWatchHandle (async version)."""

    def test_close_calls_close_func(self):
        """Test that close() calls the close function."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = AsyncWatchHandle(close_func)
        assert not close_called
        handle.close()
        assert close_called

    def test_close_only_calls_once(self):
        """Test that close() only calls the function once."""
        call_count = 0

        def close_func():
            nonlocal call_count
            call_count += 1

        handle = AsyncWatchHandle(close_func)
        handle.close()
        handle.close()
        handle.close()
        assert call_count == 1

    def test_closed_property(self):
        """Test the closed property."""
        handle = AsyncWatchHandle(lambda: None)
        assert not handle.closed
        handle.close()
        assert handle.closed

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test using AsyncWatchHandle as an async context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        async with AsyncWatchHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    @pytest.mark.asyncio
    async def test_async_context_manager_on_exception(self):
        """Test that async context manager closes on exception."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with pytest.raises(ValueError):
            async with AsyncWatchHandle(close_func):
                raise ValueError("Test error")

        assert close_called

    def test_sync_context_manager(self):
        """Test that AsyncWatchHandle also supports sync context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with AsyncWatchHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    def test_dict_like_access_backward_compatibility(self):
        """Test backward compatibility with dict-like access."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = AsyncWatchHandle(close_func)
        handle["close"]()
        assert close_called


class TestStreamHandle:
    """Tests for StreamHandle (sync version)."""

    def test_close_calls_close_func(self):
        """Test that close() calls the close function."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = StreamHandle(close_func)
        assert not close_called
        handle.close()
        assert close_called

    def test_close_only_calls_once(self):
        """Test that close() only calls the function once."""
        call_count = 0

        def close_func():
            nonlocal call_count
            call_count += 1

        handle = StreamHandle(close_func)
        handle.close()
        handle.close()
        handle.close()
        assert call_count == 1

    def test_closed_property(self):
        """Test the closed property."""
        handle = StreamHandle(lambda: None)
        assert not handle.closed
        handle.close()
        assert handle.closed

    def test_context_manager(self):
        """Test using StreamHandle as a context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with StreamHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    def test_context_manager_on_exception(self):
        """Test that context manager closes on exception."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with pytest.raises(ValueError):
            with StreamHandle(close_func):
                raise ValueError("Test error")

        assert close_called

    def test_dict_like_access_backward_compatibility(self):
        """Test backward compatibility with dict-like access."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = StreamHandle(close_func)
        handle["close"]()
        assert close_called


class TestAsyncStreamHandle:
    """Tests for AsyncStreamHandle (async version)."""

    def test_close_calls_close_func(self):
        """Test that close() calls the close function."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = AsyncStreamHandle(close_func)
        assert not close_called
        handle.close()
        assert close_called

    def test_close_only_calls_once(self):
        """Test that close() only calls the function once."""
        call_count = 0

        def close_func():
            nonlocal call_count
            call_count += 1

        handle = AsyncStreamHandle(close_func)
        handle.close()
        handle.close()
        handle.close()
        assert call_count == 1

    def test_closed_property(self):
        """Test the closed property."""
        handle = AsyncStreamHandle(lambda: None)
        assert not handle.closed
        handle.close()
        assert handle.closed

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test using AsyncStreamHandle as an async context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        async with AsyncStreamHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    @pytest.mark.asyncio
    async def test_async_context_manager_on_exception(self):
        """Test that async context manager closes on exception."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with pytest.raises(ValueError):
            async with AsyncStreamHandle(close_func):
                raise ValueError("Test error")

        assert close_called

    def test_sync_context_manager(self):
        """Test that AsyncStreamHandle also supports sync context manager."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        with AsyncStreamHandle(close_func) as handle:
            assert not close_called
            assert not handle.closed

        assert close_called

    def test_dict_like_access_backward_compatibility(self):
        """Test backward compatibility with dict-like access."""
        close_called = False

        def close_func():
            nonlocal close_called
            close_called = True

        handle = AsyncStreamHandle(close_func)
        handle["close"]()
        assert close_called
