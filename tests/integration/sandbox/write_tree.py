import asyncio
import os
from logging import getLogger

from utils import create_or_get_sandbox

from blaxel.core.sandbox import SandboxInstance
from blaxel.core.sandbox.types import SandboxFilesystemFile

logger = getLogger(__name__)

SANDBOX_NAME = "sandbox-test-python-write-tree"


async def main():
    """Main write tree test function."""
    print("🚀 Starting sandbox write tree tests...")

    try:
        # Create or get sandbox
        sandbox = await create_or_get_sandbox(SANDBOX_NAME)
        print(f"✅ Sandbox ready: {sandbox.metadata.name}")

        # Wait for sandbox to be deployed
        await sandbox.wait()
        print("✅ Sandbox deployed successfully")

        # Setup test directory
        user = os.environ.get("USER", "testuser")
        test_dir = f"/Users/{user}/Downloads/write_tree_test"

        # Clean up before test
        print("🧹 Cleaning up before test...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
        except:
            pass

        await sandbox.fs.mkdir(test_dir)
        print(f"✅ Created test directory: {test_dir}")

        # Test 1: Simple write tree
        print("🔧 Test 1: Simple write tree...")
        simple_files = [
            SandboxFilesystemFile(path="simple1.txt", content="This is simple file 1"),
            SandboxFilesystemFile(path="simple2.txt", content="This is simple file 2"),
            SandboxFilesystemFile(path="simple3.txt", content="This is simple file 3"),
        ]

        result = await sandbox.fs.write_tree(simple_files, test_dir)
        print(f"✅ Simple write tree completed: {result}")

        # Verify files were created
        directory = await sandbox.fs.ls(test_dir)
        created_files = [f.name for f in directory.files]
        print(f"Created files: {created_files}")

        for file_obj in simple_files:
            if file_obj.path in created_files:
                print(f"✅ {file_obj.path} created successfully")
                # Verify content
                content = await sandbox.fs.read(f"{test_dir}/{file_obj.path}")
                if content == file_obj.content:
                    print(f"✅ {file_obj.path} content matches")
                else:
                    print(f"❌ {file_obj.path} content mismatch")
            else:
                print(f"❌ {file_obj.path} not found")

        # Test 2: Nested directory structure
        print("🔧 Test 2: Nested directory structure...")
        nested_files = [
            SandboxFilesystemFile(
                path="config/app.json", content='{"name": "test-app", "version": "1.0.0"}'
            ),
            SandboxFilesystemFile(
                path="config/database.json", content='{"host": "localhost", "port": 5432}'
            ),
            SandboxFilesystemFile(
                path="src/main.py", content="#!/usr/bin/env python3\nprint('Hello World')"
            ),
            SandboxFilesystemFile(
                path="src/utils.py", content="def helper_function():\n    return 'helper'"
            ),
            SandboxFilesystemFile(
                path="docs/readme.md", content="# Project\n\nThis is a test project."
            ),
            SandboxFilesystemFile(
                path="docs/api.md", content="# API Documentation\n\n## Endpoints"
            ),
            SandboxFilesystemFile(
                path="tests/test_main.py",
                content="import unittest\n\nclass TestMain(unittest.TestCase):\n    pass",
            ),
        ]

        nested_dir = f"{test_dir}/nested_project"
        await sandbox.fs.mkdir(nested_dir)

        result = await sandbox.fs.write_tree(nested_files, nested_dir)
        print(f"✅ Nested write tree completed: {result}")

        # Verify nested structure
        for file_obj in nested_files:
            try:
                full_path = f"{nested_dir}/{file_obj.path}"
                content = await sandbox.fs.read(full_path)
                if content == file_obj.content:
                    print(f"✅ {file_obj.path} created with correct content")
                else:
                    print(f"❌ {file_obj.path} content mismatch")
            except Exception as e:
                print(f"❌ Failed to read {file_obj.path}: {e}")

        # Test 3: Large file tree
        print("🔧 Test 3: Large file tree...")
        large_files = []

        # Create many files
        for i in range(50):
            file_path = f"batch_{i // 10}/file_{i}.txt"
            content = f"This is file number {i}\nGenerated for batch testing\nLine 3 of file {i}"
            large_files.append(SandboxFilesystemFile(path=file_path, content=content))

        large_dir = f"{test_dir}/large_batch"
        await sandbox.fs.mkdir(large_dir)

        start_time = asyncio.get_event_loop().time()
        result = await sandbox.fs.write_tree(large_files, large_dir)
        end_time = asyncio.get_event_loop().time()

        print(f"✅ Large write tree completed in {end_time - start_time:.2f} seconds")
        print(f"Files written: {len(large_files)}")

        # Verify a sample of files
        sample_indices = [0, 10, 25, 40, 49]
        for i in sample_indices:
            file_obj = large_files[i]
            try:
                full_path = f"{large_dir}/{file_obj.path}"
                content = await sandbox.fs.read(full_path)
                if content == file_obj.content:
                    print(f"✅ Sample file {i} ({file_obj.path}) verified")
                else:
                    print(f"❌ Sample file {i} content mismatch")
            except Exception as e:
                print(f"❌ Failed to verify sample file {i}: {e}")

        # Test 4: Different file types
        print("🔧 Test 4: Different file types...")
        mixed_files = [
            SandboxFilesystemFile(
                path="data.json",
                content='{\n  "users": [\n    {"id": 1, "name": "Alice"},\n    {"id": 2, "name": "Bob"}\n  ]\n}',
            ),
            SandboxFilesystemFile(
                path="script.sh",
                content="#!/bin/bash\necho 'Running script'\nls -la\necho 'Script completed'",
            ),
            SandboxFilesystemFile(
                path="styles.css",
                content="body {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 20px;\n}",
            ),
            SandboxFilesystemFile(
                path="index.html",
                content="<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello</h1></body>\n</html>",
            ),
            SandboxFilesystemFile(
                path="data.csv",
                content="id,name,email\n1,Alice,alice@example.com\n2,Bob,bob@example.com",
            ),
            SandboxFilesystemFile(path="empty.txt", content=""),
        ]

        mixed_dir = f"{test_dir}/mixed_types"
        await sandbox.fs.mkdir(mixed_dir)

        result = await sandbox.fs.write_tree(mixed_files, mixed_dir)
        print("✅ Mixed file types write tree completed")

        # Verify mixed files
        for file_obj in mixed_files:
            try:
                full_path = f"{mixed_dir}/{file_obj.path}"
                content = await sandbox.fs.read(full_path)
                if content == file_obj.content:
                    print(f"✅ {file_obj.path} ({len(file_obj.content)} chars) verified")
                else:
                    print(f"❌ {file_obj.path} content mismatch")
            except Exception as e:
                print(f"❌ Failed to verify {file_obj.path}: {e}")

        # Test 5: Overwrite existing files
        print("🔧 Test 5: Overwrite existing files...")
        overwrite_files = [
            SandboxFilesystemFile(
                path="simple1.txt", content="This is the NEW content for simple1"
            ),
            SandboxFilesystemFile(
                path="simple2.txt", content="This is the NEW content for simple2"
            ),
            SandboxFilesystemFile(path="new_file.txt", content="This is a completely new file"),
        ]

        result = await sandbox.fs.write_tree(overwrite_files, test_dir)
        print("✅ Overwrite write tree completed")

        # Verify overwritten content
        for file_obj in overwrite_files:
            try:
                full_path = f"{test_dir}/{file_obj.path}"
                content = await sandbox.fs.read(full_path)
                if content == file_obj.content:
                    print(f"✅ {file_obj.path} overwritten successfully")
                else:
                    print(f"❌ {file_obj.path} overwrite failed")
            except Exception as e:
                print(f"❌ Failed to verify overwrite {file_obj.path}: {e}")

        # Test 6: Error handling
        print("🔧 Test 6: Error handling...")
        try:
            # Try to write to non-existent directory
            error_files = [
                SandboxFilesystemFile(path="test.txt", content="This should fail"),
            ]
            await sandbox.fs.write_tree(error_files, "/non/existent/directory")
            print("⚠️ Write tree to non-existent directory unexpectedly succeeded")
        except Exception as e:
            print(f"✅ Expected error for non-existent directory: {type(e).__name__}")

        # Clean up
        print("🧹 Cleaning up test files...")
        try:
            await sandbox.fs.rm(test_dir, recursive=True)
            print("✅ Test directory removed")
        except Exception as e:
            print(f"⚠️ Failed to remove test directory: {e}")

        print("📊 Write Tree Test Summary:")
        print(f"  Simple files: {len(simple_files)}")
        print(f"  Nested files: {len(nested_files)}")
        print(f"  Large batch files: {len(large_files)}")
        print(f"  Mixed type files: {len(mixed_files)}")
        print(f"  Overwrite files: {len(overwrite_files)}")

        print("🎉 All write tree tests completed!")

    except Exception as e:
        print(f"❌ Write tree test failed with error: {e}")
        logger.exception("Write tree test error")
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
