import asyncio
import os
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.client.models.process_request import ProcessRequest

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-comprehensive"


async def test_filesystem(sandbox: SandboxInstance):
    """Test comprehensive filesystem operations."""
    print("🔧 Testing filesystem operations...")

    user = os.environ.get("USER", "testuser")
    test_file = f"/Users/{user}/Downloads/test"
    test_dir = f"/Users/{user}/Downloads/test2"

    # Test write and read
    await sandbox.fs.write(test_file, "Hello world")
    content = await sandbox.fs.read(test_file)
    assert content == "Hello world", f"File content mismatch: {content}"

    # Test directory listing
    dir_listing = await sandbox.fs.ls(f"/Users/{user}/Downloads")
    assert any(f.path == test_file for f in dir_listing.files), "File not found in directory"

    # Test mkdir
    await sandbox.fs.mkdir(test_dir)
    after_mkdir = await sandbox.fs.ls(test_dir)
    assert hasattr(after_mkdir, "files"), "Directory creation failed"

    # Test copy
    await sandbox.fs.cp(test_file, f"{test_dir}/test")
    after_cp = await sandbox.fs.ls(test_dir)
    assert any(f.path == f"{test_dir}/test" for f in after_cp.files), "File copy failed"

    # Test remove
    await sandbox.fs.rm(test_file)

    # Test recursive remove (should fail first, then succeed)
    try:
        await sandbox.fs.rm(test_dir)
        assert False, "Should have failed to remove non-empty directory"
    except Exception as e:
        logger.info(f"Expected error: {e}")

    await sandbox.fs.rm(test_dir, recursive=True)

    print("✅ Filesystem tests passed!")


async def test_process(sandbox: SandboxInstance):
    """Test process execution and management."""
    print("🔧 Testing process operations...")

    # Test process execution
    process_request = ProcessRequest(name="test", command="echo 'Hello world'")
    process = await sandbox.process.exec(process_request)

    assert process.status != "completed", "Process completed immediately"

    # Wait a bit for completion
    await asyncio.sleep(0.1)

    completed_process = await sandbox.process.get("test")
    if completed_process.status != "completed":
        # Wait for completion
        completed_process = await sandbox.process.wait("test")

    assert completed_process.status == "completed", "Process did not complete"

    # Test logs
    logs = await sandbox.process.logs("test")
    assert "Hello world" in logs, f"Logs incorrect: {logs}"

    # Test kill (should fail for completed process)
    try:
        await sandbox.process.kill("test")
        logger.info("Kill succeeded (process may have been running)")
    except Exception as e:
        logger.info(f"Expected error killing completed process: {e}")

    print("✅ Process tests passed!")


async def test_process_logs_streaming(sandbox: SandboxInstance):
    """Test process log streaming functionality."""
    print("🔧 Testing process log streaming...")

    log_called = False
    stdout_called = False
    stderr_called = False
    log_output = ""
    stdout_output = ""
    stderr_output = ""

    # Command that outputs to both stdout and stderr
    command = 'sh -c \'for i in $(seq 1 3); do echo "Hello from stdout $i"; echo "Hello from stderr $i" 1>&2; sleep 1; done\''
    name = "test-streaming"

    process_request = ProcessRequest(name=name, command=command)
    await sandbox.process.exec(process_request)

    def on_log(log):
        nonlocal log_called, log_output
        log_called = True
        log_output += log + "\n"
        print(f"onLog: {log}")

    def on_stdout(stdout):
        nonlocal stdout_called, stdout_output
        stdout_called = True
        stdout_output += stdout + "\n"
        print(f"onStdout: {stdout}")

    def on_stderr(stderr):
        nonlocal stderr_called, stderr_output
        stderr_called = True
        stderr_output += stderr + "\n"
        print(f"onStderr: {stderr}")

    stream = sandbox.process.stream_logs(
        name, {"on_log": on_log, "on_stdout": on_stdout, "on_stderr": on_stderr}
    )

    await sandbox.process.wait(name)
    stream["close"]()

    # Check that handlers were called
    assert log_called, "onLog was not called"
    assert stdout_called, "onStdout was not called"
    assert stderr_called, "onStderr was not called"
    assert "Hello from stdout" in log_output, f"Log output incorrect: {log_output}"
    assert "Hello from stdout" in stdout_output, f"Stdout output incorrect: {stdout_output}"
    assert "Hello from stderr" in stderr_output, f"Stderr output incorrect: {stderr_output}"

    print("✅ Process streaming tests passed!")


async def test_previews_public(sandbox: SandboxInstance):
    """Test public preview functionality."""
    print("🔧 Testing public previews...")

    try:
        await sandbox.previews.create(
            {
                "metadata": {"name": "preview-test-public"},
                "spec": {"port": 443, "prefix_url": "small-prefix-python", "public": True},
            }
        )

        previews = await sandbox.previews.list()
        assert len(previews) >= 1, "No previews found"

        retrieved_preview = await sandbox.previews.get("preview-test-public")
        assert retrieved_preview.name == "preview-test-public", "Preview name mismatch"

        url = retrieved_preview.spec.url
        assert url is not None, "Preview URL is None"

        print(f"Preview URL: {url}")

        # Test if preview is accessible (may fail in test environment)
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{url}/health", timeout=10.0)
                if response.status_code == 200:
                    print("✅ Preview is healthy!")
                else:
                    print(f"⚠️ Preview returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Could not test preview health: {e}")

    except Exception as e:
        print(f"❌ Preview test error: {e}")
    finally:
        try:
            await sandbox.previews.delete("preview-test-public")
        except:
            pass

    print("✅ Public preview tests completed!")


async def test_previews_private(sandbox: SandboxInstance):
    """Test private preview with token functionality."""
    print("🔧 Testing private previews with tokens...")

    try:
        # Create private preview with token
        await sandbox.previews.create(
            {
                "metadata": {"name": "preview-test-private"},
                "spec": {"port": 443, "prefix_url": "private-prefix-python", "public": False},
            }
        )

        # Create token for private preview
        token = await sandbox.previews.create_token("preview-test-private")
        print(f"Preview token created: {token.token[:20]}...")

        # Get preview with token
        private_preview = await sandbox.previews.get("preview-test-private")
        assert private_preview.name == "preview-test-private", "Private preview name mismatch"

        url = private_preview.spec.url
        print(f"Private Preview URL: {url}")

        # Test private preview access with token
        try:
            import httpx

            headers = {"Authorization": f"Bearer {token.token}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{url}/health", headers=headers, timeout=10.0)
                if response.status_code == 200:
                    print("✅ Private preview accessible with token!")
                else:
                    print(f"⚠️ Private preview returned status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Could not test private preview health: {e}")

    except Exception as e:
        print(f"❌ Private preview test error: {e}")
    finally:
        try:
            await sandbox.previews.delete("preview-test-private")
        except:
            pass

    print("✅ Private preview tests completed!")


async def test_watch(sandbox: SandboxInstance):
    """Test filesystem watch functionality."""
    print("🔧 Testing filesystem watch...")

    watch_events = []

    def watch_callback(file_event):
        watch_events.append(file_event)
        print(f"Watch event: {file_event.op} {file_event.path}/{file_event.name}")

    def watch_callback_with_content(file_event):
        watch_events.append(file_event)
        print(
            f"Watch event with content: {file_event.op} {file_event.name} - {file_event.content[:50] if file_event.content else 'No content'}"
        )

    # Start watching
    handle = sandbox.fs.watch("/tmp", watch_callback)

    # Trigger some file operations
    await sandbox.fs.write("/tmp/watch-test.txt", "Initial content")
    await asyncio.sleep(1)

    await sandbox.fs.write("/tmp/watch-test.txt", "Modified content")
    await asyncio.sleep(1)

    await sandbox.fs.rm("/tmp/watch-test.txt")
    await asyncio.sleep(1)

    # Stop watching
    handle["close"]()

    print(f"Captured {len(watch_events)} watch events")
    for event in watch_events:
        print(f"  - {event.op}: {event.name}")

    print("✅ Watch tests completed!")


async def main():
    """Main comprehensive test function."""
    print("🚀 Starting comprehensive sandbox tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Run all test suites
        await test_filesystem(sandbox)
        print()

        await test_process(sandbox)
        print()

        await test_process_logs_streaming(sandbox)
        print()

        await test_previews_public(sandbox)
        print()

        await test_previews_private(sandbox)
        print()

        await test_watch(sandbox)
        print()

        print("🎉 All comprehensive tests completed successfully!")

    except Exception as e:
        print(f"❌ Comprehensive test failed with error: {e}")
        logger.exception("Comprehensive test error")
        raise
    finally:
        print("🧹 Final cleanup...")
        try:
            await SandboxInstance.delete(SANDBOX_NAME)
            print("✅ Sandbox deleted")
        except Exception as e:
            print(f"⚠️ Failed to delete sandbox: {e}")


if __name__ == "__main__":
    asyncio.run(main())
