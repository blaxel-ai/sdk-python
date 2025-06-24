import asyncio
from datetime import datetime, timedelta, timezone
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance, SessionCreateOptions
from blaxel.core.sandbox.client.models.process_request import ProcessRequest

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-session"


async def main():
    """Main session test function."""
    print("🚀 Starting sandbox session tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Clean up existing sessions
        print("🧹 Cleaning up existing sessions...")
        sessions = await sandbox.sessions.list()
        for session in sessions:
            print(f"Removing session: {session.name}")
            await sandbox.sessions.delete(session.name)

        # Create a new session
        print("🔧 Creating new session...")
        expires_at = datetime.now(timezone.utc) + timedelta(days=1)
        options = SessionCreateOptions(expires_at=expires_at)
        session = await sandbox.sessions.create(options)

        print("✅ Session created:")
        print(f"  Name: {session.name}")
        print(f"  URL: {session.url}")
        print(f"  Token: {session.token[:20]}...")
        print(f"  Expires: {session.expires_at}")

        # Create sandbox instance from session
        print("🔧 Creating sandbox instance from session...")
        sandbox_with_session = await SandboxInstance.from_session(session)

        # Test filesystem operations with session
        print("🔧 Testing filesystem operations with session...")
        test_content = "session test content"
        test_path = "/tmp/session-test.txt"
        await sandbox_with_session.fs.write(test_path, test_content)
        read_content = await sandbox_with_session.fs.read(test_path)

        if read_content == test_content:
            print("✅ Session write/read operations working")
        else:
            print(f"❌ Session write/read failed: expected '{test_content}', got '{read_content}'")

        # Test process execution with session
        print("🔧 Testing process execution with session...")
        command = 'sh -c \'for i in $(seq 1 3); do echo "Hello from stdout $i"; echo "Hello from stderr $i" 1>&2; sleep 1; done\''
        name = "test-session-process"

        process_request = ProcessRequest(name=name, command=command)
        await sandbox_with_session.process.exec(process_request)

        # Stream logs
        print("🔧 Streaming process logs...")

        def on_log(log):
            print(f"Session Log: {log}")

        stream = sandbox_with_session.process.stream_logs(name, {"on_log": on_log})
        await sandbox_with_session.process.wait(name)
        stream["close"]()

        # Test filesystem watch with session
        print("🔧 Testing filesystem watch with session...")

        def watch_callback(file_event):
            print(f"Session Watch: {file_event.op} {file_event.path}/{file_event.name}")

        handle = sandbox_with_session.fs.watch("/tmp", watch_callback)

        # Trigger a file change
        await sandbox_with_session.fs.write("/tmp/test-session.txt", "session content")

        # Wait for watch callback
        await asyncio.sleep(2)
        handle["close"]()

        # Test creating another session (simpler expiration test)
        print("🔧 Testing additional session creation...")
        simple_session = await sandbox.sessions.create(
            SessionCreateOptions(expires_at=datetime.now(timezone.utc) + timedelta(hours=2))
        )
        print("✅ Additional session created:")
        print(f"  Name: {simple_session.name}")
        print(f"  Expires: {simple_session.expires_at}")

        print("🎉 All session tests completed successfully!")

    except Exception as e:
        print(f"❌ Session test failed with error: {e}")
        logger.exception("Session test error")
        raise
    finally:
        print("🧹 Cleaning up...")
        try:
            # Clean up sessions
            sessions = await sandbox.sessions.list()
            for session in sessions:
                await sandbox.sessions.delete(session.name)
            print("✅ Sessions cleaned up")
        except Exception as e:
            print(f"⚠️ Failed to clean up sessions: {e}")

        try:
            await SandboxInstance.delete(SANDBOX_NAME)
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️ Failed to delete sandbox: {e}")


if __name__ == "__main__":
    asyncio.run(main())
