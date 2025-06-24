import asyncio
import os
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-watch-folder"


async def main():
    """Main watch folder test function."""
    print("🚀 Starting sandbox watch folder tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Setup test directory
        user = os.environ.get("USER", "testuser")
        test_dir = f"/Users/{user}/Downloads/watch_test"

        # Clean up before test
        print("🧹 Cleaning up before test...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
        except:
            pass

        await sandbox.fs.mkdir(test_dir)
        print(f"✅ Created test directory: {test_dir}")

        # Test 1: Basic file watch
        print("🔧 Test 1: Basic file watch...")
        watch_events = []

        def basic_watch_callback(file_event):
            watch_events.append(file_event)
            print(f"Watch event: {file_event.op} {file_event.path}/{file_event.name}")

        # Start watching
        handle = sandbox.fs.watch(test_dir, basic_watch_callback)

        # Create some files
        await sandbox.fs.write(f"{test_dir}/test1.txt", "Initial content")
        await asyncio.sleep(1)

        await sandbox.fs.write(f"{test_dir}/test2.txt", "Another file")
        await asyncio.sleep(1)

        # Modify a file
        await sandbox.fs.write(f"{test_dir}/test1.txt", "Modified content")
        await asyncio.sleep(1)

        # Delete a file
        await sandbox.fs.rm(f"{test_dir}/test2.txt")
        await asyncio.sleep(1)

        # Stop watching
        handle["close"]()

        print(f"Basic watch captured {len(watch_events)} events")
        for event in watch_events:
            print(f"  - {event.op}: {event.name}")

        # Test 2: Watch with content
        print("🔧 Test 2: Watch with content...")
        content_events = []

        def content_watch_callback(file_event):
            content_events.append(file_event)
            content_preview = file_event.content[:50] if file_event.content else "No content"
            print(f"Content watch: {file_event.op} {file_event.name} - {content_preview}")

        # Start watching with content
        content_handle = sandbox.fs.watch(test_dir, content_watch_callback, {"with_content": True})

        # Create files with specific content
        await sandbox.fs.write(
            f"{test_dir}/content1.txt", "This is the first file with some content"
        )
        await asyncio.sleep(1)

        await sandbox.fs.write(f"{test_dir}/content2.json", '{"key": "value", "number": 42}')
        await asyncio.sleep(1)

        # Modify with new content
        await sandbox.fs.write(
            f"{test_dir}/content1.txt", "This is the modified content of the first file"
        )
        await asyncio.sleep(1)

        content_handle["close"]()

        print(f"Content watch captured {len(content_events)} events")
        for event in content_events:
            content_preview = event.content[:30] if event.content else "No content"
            print(f"  - {event.op}: {event.name} ({content_preview}...)")

        # Test 3: Watch subdirectories
        print("🔧 Test 3: Watch subdirectories...")
        subdir_events = []

        def subdir_watch_callback(file_event):
            subdir_events.append(file_event)
            print(f"Subdir watch: {file_event.op} {file_event.path}/{file_event.name}")

        # Create subdirectory
        sub_dir = f"{test_dir}/subdir"
        await sandbox.fs.mkdir(sub_dir)

        # Start watching the parent directory
        subdir_handle = sandbox.fs.watch(test_dir, subdir_watch_callback)

        # Create files in subdirectory
        await sandbox.fs.write(f"{sub_dir}/sub1.txt", "File in subdirectory")
        await asyncio.sleep(1)

        await sandbox.fs.write(f"{sub_dir}/sub2.txt", "Another file in subdirectory")
        await asyncio.sleep(1)

        # Create nested subdirectory
        nested_dir = f"{sub_dir}/nested"
        await sandbox.fs.mkdir(nested_dir)
        await sandbox.fs.write(f"{nested_dir}/nested.txt", "Nested file")
        await asyncio.sleep(1)

        subdir_handle["close"]()

        print(f"Subdirectory watch captured {len(subdir_events)} events")
        for event in subdir_events:
            print(f"  - {event.op}: {event.path}/{event.name}")

        # Test 4: Multiple watchers on same directory
        print("🔧 Test 4: Multiple watchers...")
        watcher1_events = []
        watcher2_events = []

        def watcher1_callback(file_event):
            watcher1_events.append(file_event)
            print(f"Watcher 1: {file_event.op} {file_event.name}")

        def watcher2_callback(file_event):
            watcher2_events.append(file_event)
            print(f"Watcher 2: {file_event.op} {file_event.name}")

        # Start multiple watchers
        handle1 = sandbox.fs.watch(test_dir, watcher1_callback)
        handle2 = sandbox.fs.watch(test_dir, watcher2_callback, {"with_content": True})

        # Trigger events
        await sandbox.fs.write(f"{test_dir}/multi.txt", "File watched by multiple watchers")
        await asyncio.sleep(1)

        await sandbox.fs.write(f"{test_dir}/multi.txt", "Modified by multiple watchers")
        await asyncio.sleep(1)

        # Stop both watchers
        handle1["close"]()
        handle2["close"]()

        print(f"Watcher 1 captured {len(watcher1_events)} events")
        print(f"Watcher 2 captured {len(watcher2_events)} events")

        # Test 5: Watch with ignore patterns
        print("🔧 Test 5: Watch with ignore patterns...")
        ignore_events = []

        def ignore_watch_callback(file_event):
            ignore_events.append(file_event)
            print(f"Ignore watch: {file_event.op} {file_event.name}")

        # Start watching with ignore patterns
        ignore_handle = sandbox.fs.watch(
            test_dir, ignore_watch_callback, {"ignore": ["*.tmp", "*.log"]}
        )

        # Create files that should be watched
        await sandbox.fs.write(f"{test_dir}/important.txt", "This should be watched")
        await asyncio.sleep(1)

        # Create files that should be ignored
        await sandbox.fs.write(f"{test_dir}/temp.tmp", "This should be ignored")
        await asyncio.sleep(1)

        await sandbox.fs.write(f"{test_dir}/debug.log", "This should also be ignored")
        await asyncio.sleep(1)

        # Create another watched file
        await sandbox.fs.write(f"{test_dir}/another.txt", "This should also be watched")
        await asyncio.sleep(1)

        ignore_handle["close"]()

        print(f"Ignore pattern watch captured {len(ignore_events)} events")
        watched_files = [event.name for event in ignore_events]
        print(f"Watched files: {watched_files}")

        # Verify ignore patterns worked
        if "temp.tmp" not in watched_files and "debug.log" not in watched_files:
            print("✅ Ignore patterns working correctly")
        else:
            print("⚠️ Ignore patterns may not be working as expected")

        # Clean up
        print("🧹 Cleaning up test files...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
            print("✅ Test directory removed")
        except Exception as e:
            print(f"⚠️ Failed to remove test directory: {e}")

        print("📊 Watch Test Summary:")
        print(f"  Basic watch events: {len(watch_events)}")
        print(f"  Content watch events: {len(content_events)}")
        print(f"  Subdirectory watch events: {len(subdir_events)}")
        print(f"  Multi-watcher events: W1={len(watcher1_events)}, W2={len(watcher2_events)}")
        print(f"  Ignore pattern events: {len(ignore_events)}")

        print("🎉 All watch folder tests completed!")

    except Exception as e:
        print(f"❌ Watch folder test failed with error: {e}")
        logger.exception("Watch folder test error")
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
