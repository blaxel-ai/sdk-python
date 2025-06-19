import asyncio
import os
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-read-multiple"


async def main():
    """Main read multiple files test function."""
    print("🚀 Starting sandbox read multiple files tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Setup test directory
        user = os.environ.get("USER", "testuser")
        test_dir = f"/Users/{user}/Downloads/read_test"

        # Clean up before test
        print("🧹 Cleaning up before test...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
        except:
            pass

        await sandbox.fs.mkdir(test_dir)
        print(f"✅ Created test directory: {test_dir}")

        # Create multiple test files with different content
        print("🔧 Creating test files...")
        test_files = {
            "file1.txt": "This is the content of file 1.\nIt has multiple lines.\nLine 3 of file 1.",
            "file2.json": '{\n  "name": "test",\n  "version": "1.0.0",\n  "description": "A test JSON file"\n}',
            "file3.md": "# Test Markdown File\n\nThis is a **markdown** file with some content.\n\n## Section 2\n\n- Item 1\n- Item 2\n- Item 3",
            "file4.py": "#!/usr/bin/env python3\n\ndef hello_world():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    hello_world()",
            "file5.csv": "Name,Age,City\nJohn,25,New York\nJane,30,San Francisco\nBob,35,Chicago",
            "empty.txt": "",
            "large.txt": "Large file content.\n" * 1000,  # Create a larger file
        }

        # Write all files
        for filename, content in test_files.items():
            file_path = f"{test_dir}/{filename}"
            await sandbox.fs.write(file_path, content)
            print(f"✅ Created {filename} ({len(content)} chars)")

        # Test 1: Read all files sequentially
        print("🔧 Test 1: Reading files sequentially...")
        sequential_results = {}
        sequential_start_time = asyncio.get_event_loop().time()

        for filename in test_files.keys():
            file_path = f"{test_dir}/{filename}"
            content = await sandbox.fs.read(file_path)
            sequential_results[filename] = content
            print(f"✅ Read {filename} ({len(content)} chars)")

        sequential_time = asyncio.get_event_loop().time() - sequential_start_time
        print(f"Sequential read time: {sequential_time:.2f} seconds")

        # Test 2: Read all files concurrently
        print("🔧 Test 2: Reading files concurrently...")
        concurrent_start_time = asyncio.get_event_loop().time()

        async def read_file(filename):
            file_path = f"{test_dir}/{filename}"
            content = await sandbox.fs.read(file_path)
            return filename, content

        # Create tasks for concurrent reading
        tasks = [read_file(filename) for filename in test_files.keys()]
        concurrent_results_list = await asyncio.gather(*tasks)
        concurrent_results = dict(concurrent_results_list)

        concurrent_time = asyncio.get_event_loop().time() - concurrent_start_time
        print(f"Concurrent read time: {concurrent_time:.2f} seconds")

        # Verify results match
        print("🔧 Verifying results...")
        for filename in test_files.keys():
            original = test_files[filename]
            sequential = sequential_results[filename]
            concurrent = concurrent_results[filename]

            if original == sequential == concurrent:
                print(f"✅ {filename}: All reads match")
            else:
                print(f"❌ {filename}: Content mismatch")
                print(f"  Original length: {len(original)}")
                print(f"  Sequential length: {len(sequential)}")
                print(f"  Concurrent length: {len(concurrent)}")

        # Test 3: Read files in subdirectories
        print("🔧 Test 3: Testing nested directory reads...")
        nested_dir = f"{test_dir}/nested"
        await sandbox.fs.mkdir(nested_dir)

        nested_files = {
            "nested/config.ini": "[section1]\nkey1=value1\nkey2=value2\n\n[section2]\nkey3=value3",
            "nested/data.xml": "<?xml version='1.0'?>\n<root>\n  <item id='1'>Value 1</item>\n  <item id='2'>Value 2</item>\n</root>",
        }

        for rel_path, content in nested_files.items():
            file_path = f"{test_dir}/{rel_path}"
            await sandbox.fs.write(file_path, content)
            print(f"✅ Created nested file {rel_path}")

        # Read nested files
        nested_results = {}
        for rel_path in nested_files.keys():
            file_path = f"{test_dir}/{rel_path}"
            content = await sandbox.fs.read(file_path)
            nested_results[rel_path] = content
            print(f"✅ Read nested {rel_path} ({len(content)} chars)")

        # Verify nested file contents
        for rel_path in nested_files.keys():
            if nested_files[rel_path] == nested_results[rel_path]:
                print(f"✅ {rel_path}: Content matches")
            else:
                print(f"❌ {rel_path}: Content mismatch")

        # Test 4: Error handling for non-existent files
        print("🔧 Test 4: Testing error handling...")
        non_existent_files = [
            f"{test_dir}/does_not_exist.txt",
            f"{test_dir}/missing/file.txt",
            "/completely/invalid/path.txt",
        ]

        for file_path in non_existent_files:
            try:
                content = await sandbox.fs.read(file_path)
                print(f"⚠️ Unexpectedly succeeded reading {file_path}")
            except Exception as e:
                print(f"✅ Expected error reading {file_path}: {type(e).__name__}")

        # Test 5: Performance comparison
        print("🔧 Test 5: Performance analysis...")
        if concurrent_time < sequential_time:
            speedup = sequential_time / concurrent_time
            print(f"✅ Concurrent reading is {speedup:.2f}x faster than sequential")
        else:
            print(
                "⚠️ Sequential reading was faster (may be due to small file sizes or network overhead)"
            )

        print("📊 Performance Summary:")
        print(f"  Files read: {len(test_files)}")
        print(f"  Sequential time: {sequential_time:.2f}s")
        print(f"  Concurrent time: {concurrent_time:.2f}s")
        print(f"  Total content size: {sum(len(content) for content in test_files.values())} chars")

        # Clean up
        print("🧹 Cleaning up test files...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
            print("✅ Test directory removed")
        except Exception as e:
            print(f"⚠️ Failed to remove test directory: {e}")

        print("🎉 All read multiple files tests completed!")

    except Exception as e:
        print(f"❌ Read multiple files test failed with error: {e}")
        logger.exception("Read multiple files test error")
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
