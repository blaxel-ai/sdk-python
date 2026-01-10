from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import async_sleep, default_image, default_labels, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestSessionOperations:
    """Test sandbox session operations."""

    sandbox: SandboxInstance = None
    sandbox_name: str = None

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def setup_sandbox(self, request):
        """Set up a sandbox for the test class."""
        request.cls.sandbox_name = unique_name("session-test")
        request.cls.sandbox = await SandboxInstance.create(
            {
                "name": request.cls.sandbox_name,
                "image": default_image,
                "memory": 2048,
                "labels": default_labels,
            }
        )

        yield

        # Cleanup
        try:
            await SandboxInstance.delete(request.cls.sandbox_name)
        except Exception:
            pass


@pytest.mark.asyncio(loop_scope="class")
class TestSessionCreate(TestSessionOperations):
    """Test session creation operations."""

    async def test_creates_session_with_expiration(self):
        """Test creating a session with expiration."""
        expires_at = datetime.now(timezone.utc) + timedelta(days=1)

        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        assert session.name is not None
        assert session.token is not None
        assert session.url is not None

        await self.sandbox.sessions.delete(session.name)

    async def test_session_has_valid_url_and_token(self):
        """Test that session has valid URL and token."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        assert "http" in session.url
        assert len(session.token) > 0

        await self.sandbox.sessions.delete(session.name)


@pytest.mark.asyncio(loop_scope="class")
class TestSessionList(TestSessionOperations):
    """Test session list operations."""

    async def test_lists_all_sessions(self):
        """Test listing all sessions."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        session1 = await self.sandbox.sessions.create({"expires_at": expires_at})
        session2 = await self.sandbox.sessions.create({"expires_at": expires_at})

        sessions = await self.sandbox.sessions.list()

        assert len(sessions) >= 2
        assert any(s.name == session1.name for s in sessions)
        assert any(s.name == session2.name for s in sessions)

        await self.sandbox.sessions.delete(session1.name)
        await self.sandbox.sessions.delete(session2.name)


@pytest.mark.asyncio(loop_scope="class")
class TestSessionDelete(TestSessionOperations):
    """Test session delete operations."""

    async def test_deletes_session(self):
        """Test deleting a session."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        await self.sandbox.sessions.delete(session.name)

        sessions = await self.sandbox.sessions.list()
        assert not any(s.name == session.name for s in sessions)


@pytest.mark.asyncio(loop_scope="class")
class TestFromSession(TestSessionOperations):
    """Test fromSession operations."""

    async def test_creates_sandbox_instance_from_session(self):
        """Test creating a sandbox instance from a session."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        sandbox_from_session = await SandboxInstance.from_session(session)

        # Should be able to perform operations
        listing = await sandbox_from_session.fs.ls("/")
        assert listing.subdirectories is not None

        await self.sandbox.sessions.delete(session.name)

    async def test_session_sandbox_can_execute_processes(self):
        """Test that session sandbox can execute processes."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        sandbox_from_session = await SandboxInstance.from_session(session)

        result = await sandbox_from_session.process.exec(
            {
                "command": "echo 'from session'",
                "wait_for_completion": True,
            }
        )

        assert "from session" in result.logs

        await self.sandbox.sessions.delete(session.name)

    async def test_session_sandbox_can_stream_logs(self):
        """Test that session sandbox can stream logs."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        sandbox_from_session = await SandboxInstance.from_session(session)

        await sandbox_from_session.process.exec(
            {
                "name": "stream-session",
                "command": "for i in 1 2 3; do echo $i; sleep 1; done",
                "wait_for_completion": False,
            }
        )

        logs = []
        stream = sandbox_from_session.process.stream_logs(
            "stream-session",
            {
                "on_log": lambda log: logs.append(log),
            },
        )

        await sandbox_from_session.process.wait("stream-session")
        await async_sleep(0.1)
        stream["close"]()

        assert len(logs) > 0

        await self.sandbox.sessions.delete(session.name)

    async def test_session_sandbox_can_watch_files(self):
        """Test that session sandbox can watch files."""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session = await self.sandbox.sessions.create({"expires_at": expires_at})

        sandbox_from_session = await SandboxInstance.from_session(session)

        change_detected = False

        def on_change(event):
            nonlocal change_detected
            change_detected = True

        handle = sandbox_from_session.fs.watch("/", on_change)
        await async_sleep(0.5)  # Wait for watch to be established
        await sandbox_from_session.fs.write("/session-test.txt", "content")

        await async_sleep(1.0)  # Wait for callback to fire
        handle["close"]()

        assert change_detected is True

        await self.sandbox.sessions.delete(session.name)
