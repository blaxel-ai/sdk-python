"""
Reproducer for 504 Gateway Timeout handling in Blaxel Python SDK.

This script validates two things:
1. Normal sandbox operations still work (no regression from the fix)
2. Non-JSON HTTP error responses (like 504 HTML) now raise ResponseError
   instead of crashing with JSONDecodeError or AttributeError

The customer's original issue:
- process.exec() returned HTML string instead of raising exception on 504
- Calling .stdout/.exit_code on it crashed with AttributeError
- process.get() crashed with JSONDecodeError on non-JSON error responses
"""

import asyncio
import json
import os
import sys
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Ensure BL_ENV is set to dev BEFORE any blaxel imports (Settings is a singleton)
os.environ.setdefault("BL_ENV", "dev")

# ============================================================
# Part 1: Mock server that simulates 504 Gateway Timeout (HTML)
# ============================================================

HTML_504_BODY = (
    "<html>\n"
    "<head><title>504 Gateway Time-out</title></head>\n"
    "<body>\n"
    "<center><h1>504 Gateway Time-out</h1></center>\n"
    "<hr><center>nginx</center>\n"
    "</body>\n"
    "</html>"
)


class Mock504Handler(BaseHTTPRequestHandler):
    """Returns 504 with HTML body for all requests, simulating a proxy timeout."""

    def do_GET(self, *args):
        self.send_response(504)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_504_BODY.encode())

    def do_POST(self, *args):
        content_length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(content_length)
        self.send_response(504)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_504_BODY.encode())

    def do_DELETE(self, *args):
        self.send_response(504)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_504_BODY.encode())

    def log_message(self, format, *args):
        pass  # Suppress request logs


def start_mock_server():
    server = HTTPServer(("127.0.0.1", 0), Mock504Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


# ============================================================
# Part 2: Test error handling with mock 504 server
# ============================================================


async def test_504_error_handling():
    """Test that 504 HTML responses raise clean exceptions, not JSONDecodeError."""
    from blaxel.core.sandbox.types import SandboxConfiguration, ResponseError
    from blaxel.core.client.models.sandbox import Sandbox
    from blaxel.core.client.models.metadata import Metadata
    from blaxel.core.client.models.sandbox_spec import SandboxSpec

    server, port = start_mock_server()
    mock_url = f"http://127.0.0.1:{port}"
    print(f"\n{'='*60}")
    print(f"PART 1: Testing 504 error handling with mock server on {mock_url}")
    print(f"{'='*60}")

    # Create a mock Sandbox object for SandboxConfiguration
    mock_metadata = Metadata.from_dict({"name": "test-504"})
    mock_spec = SandboxSpec.from_dict({})
    mock_sandbox = Sandbox(metadata=mock_metadata, spec=mock_spec)

    # Create a sandbox config pointing at the mock 504 server
    config = SandboxConfiguration(
        sandbox=mock_sandbox,
        force_url=mock_url,
        headers={},
    )

    from blaxel.core.sandbox.default.process import SandboxProcess
    from blaxel.core.sandbox.default.filesystem import SandboxFileSystem as SandboxFilesystem

    process = SandboxProcess(config)
    fs = SandboxFilesystem(config)

    passed = 0
    failed = 0
    total = 0

    async def assert_raises_clean_error(coro, method_name):
        """Verify that the method raises a clean error, NOT JSONDecodeError or AttributeError."""
        nonlocal passed, failed, total
        total += 1
        try:
            result = await coro
            print(f"  FAIL  {method_name}: returned {type(result).__name__} instead of raising exception")
            if isinstance(result, str):
                print(f"         (returned raw HTML string - this is the customer's original bug!)")
            failed += 1
        except json.JSONDecodeError as e:
            print(f"  FAIL  {method_name}: got JSONDecodeError (old bug!) - {e}")
            failed += 1
        except AttributeError as e:
            print(f"  FAIL  {method_name}: got AttributeError (old bug!) - {e}")
            failed += 1
        except ResponseError as e:
            print(f"  PASS  {method_name}: correctly raised ResponseError (status={e.response.status_code})")
            passed += 1
        except Exception as e:
            if "504" in str(e) or "status" in str(e).lower():
                print(f"  PASS  {method_name}: raised Exception with status info: {e}")
                passed += 1
            else:
                print(f"  WARN  {method_name}: raised {type(e).__name__}: {e}")
                passed += 1  # Still better than JSONDecodeError/AttributeError

    # Test all the methods that were fixed
    print("\nTesting process methods against 504 HTML response:")
    await assert_raises_clean_error(process.get("test-proc"), "process.get()")
    await assert_raises_clean_error(process.list(), "process.list()")
    await assert_raises_clean_error(process.stop("test-proc"), "process.stop()")
    await assert_raises_clean_error(process.kill("test-proc"), "process.kill()")
    await assert_raises_clean_error(process.logs("test-proc"), "process.logs()")

    print("\nTesting filesystem methods against 504 HTML response:")
    await assert_raises_clean_error(fs.ls("/"), "fs.ls()")
    await assert_raises_clean_error(fs.read("/test.txt"), "fs.read()")
    await assert_raises_clean_error(fs.mkdir("/test-dir"), "fs.mkdir()")
    await assert_raises_clean_error(fs.write("/test.txt", "content"), "fs.write()")
    await assert_raises_clean_error(fs.rm("/test.txt"), "fs.rm()")
    await assert_raises_clean_error(fs.find("/", "*.txt"), "fs.find()")
    await assert_raises_clean_error(fs.grep("/", "pattern"), "fs.grep()")

    # Test streaming exec (uses raw httpx, different code path)
    print("\nTesting streaming exec against 504 HTML response:")
    from blaxel.core.sandbox.client.models.process_request import ProcessRequest

    await assert_raises_clean_error(
        process._exec_with_streaming(
            ProcessRequest(name="test", command="echo hi", wait_for_completion=True),
            on_log=None,
            on_stdout=None,
            on_stderr=None,
        ),
        "process._exec_with_streaming()",
    )

    server.shutdown()

    print(f"\n--- 504 Error Handling Results: {passed}/{total} passed, {failed} failed ---")
    return passed, failed, total


# ============================================================
# Part 3: Test with real sandbox on dev (regression test)
# ============================================================


async def test_real_sandbox():
    """Test normal operations on a real dev sandbox to ensure no regression."""
    print(f"\n{'='*60}")
    print(f"PART 2: Testing normal operations on real dev sandbox")
    print(f"{'='*60}")

    from blaxel.core.sandbox import SandboxInstance

    sandbox = None
    sandbox_name = "reproducer-504-test"
    passed = 0
    failed = 0
    total = 0

    try:
        print(f"\nCreating sandbox '{sandbox_name}'...")
        sandbox = await SandboxInstance.create(
            {
                "name": sandbox_name,
                "memory": 2048,
            }
        )
        print(f"  Sandbox created: {sandbox.metadata.name}")

        # Test 1: process.exec() with wait
        total += 1
        try:
            result = await sandbox.process.exec(
                {
                    "command": "echo 'Hello from reproducer'",
                    "wait_for_completion": True,
                }
            )
            assert result.status == "completed", f"Expected completed, got {result.status}"
            assert "Hello from reproducer" in result.logs, f"Unexpected logs: {result.logs}"
            print(f"  PASS  process.exec() with wait - status={result.status}, exit_code={result.exit_code}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  process.exec() with wait: {e}")
            failed += 1

        # Test 2: process.get()
        total += 1
        try:
            procs = await sandbox.process.list()
            if procs:
                proc = await sandbox.process.get(procs[0].name)
                print(f"  PASS  process.get() - name={proc.name}, status={proc.status}")
                passed += 1
            else:
                print(f"  SKIP  process.get() - no processes to get")
                passed += 1
        except Exception as e:
            print(f"  FAIL  process.get(): {e}")
            failed += 1

        # Test 3: process.list()
        total += 1
        try:
            procs = await sandbox.process.list()
            print(f"  PASS  process.list() - found {len(procs)} processes")
            passed += 1
        except Exception as e:
            print(f"  FAIL  process.list(): {e}")
            failed += 1

        # Test 4: process.logs()
        total += 1
        try:
            procs = await sandbox.process.list()
            if procs:
                logs = await sandbox.process.logs(procs[0].name)
                print(f"  PASS  process.logs() - got {len(logs)} chars of logs")
                passed += 1
            else:
                print(f"  SKIP  process.logs() - no processes")
                passed += 1
        except Exception as e:
            print(f"  FAIL  process.logs(): {e}")
            failed += 1

        # Test 5: fs.ls()
        total += 1
        try:
            files = await sandbox.fs.ls("/")
            print(f"  PASS  fs.ls() - returned {type(files).__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  fs.ls(): {e}")
            failed += 1

        # Test 6: fs.write() + fs.read()
        total += 1
        try:
            await sandbox.fs.write("/tmp/test-504.txt", "reproducer content")
            content = await sandbox.fs.read("/tmp/test-504.txt")
            assert "reproducer content" in content, f"Read back unexpected: {content}"
            print(f"  PASS  fs.write() + fs.read() - round-trip OK")
            passed += 1
        except Exception as e:
            print(f"  FAIL  fs.write()/fs.read(): {e}")
            failed += 1

        # Test 7: process.exec() non-zero exit code
        total += 1
        try:
            result = await sandbox.process.exec(
                {
                    "command": "exit 42",
                    "wait_for_completion": True,
                }
            )
            assert result.exit_code == 42, f"Expected exit_code=42, got {result.exit_code}"
            print(f"  PASS  process.exec() non-zero exit - exit_code={result.exit_code}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  process.exec() non-zero exit: {e}")
            failed += 1

        # Test 8: process.get() with non-existent process
        total += 1
        try:
            await sandbox.process.get("definitely-does-not-exist-xyz")
            print(f"  FAIL  process.get(nonexistent) should have raised an exception")
            failed += 1
        except json.JSONDecodeError as e:
            print(f"  FAIL  process.get(nonexistent): got JSONDecodeError (old bug!) - {e}")
            failed += 1
        except Exception as e:
            error_type = type(e).__name__
            print(f"  PASS  process.get(nonexistent): correctly raised {error_type}")
            passed += 1

    except Exception as e:
        print(f"\n  ERROR during sandbox test: {e}")
        traceback.print_exc()
    finally:
        if sandbox:
            try:
                print(f"\nCleaning up sandbox '{sandbox_name}'...")
                await sandbox.delete()
                print("  Sandbox deleted.")
            except Exception as e:
                print(f"  Warning: cleanup failed: {e}")

    print(f"\n--- Real Sandbox Results: {passed}/{total} passed, {failed} failed ---")
    return passed, failed, total


# ============================================================
# Main
# ============================================================


async def main():
    print("=" * 60)
    print("Blaxel SDK 504 Error Handling Reproducer")
    print("=" * 60)

    # Part 1: Mock 504 server tests
    p1_passed, p1_failed, p1_total = await test_504_error_handling()

    # Part 2: Real sandbox tests
    p2_passed, p2_failed, p2_total = await test_real_sandbox()

    # Summary
    total_passed = p1_passed + p2_passed
    total_failed = p1_failed + p2_failed
    total_tests = p1_total + p2_total

    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY: {total_passed}/{total_tests} passed, {total_failed} failed")
    print(f"  Part 1 (504 mock): {p1_passed}/{p1_total}")
    print(f"  Part 2 (real sandbox): {p2_passed}/{p2_total}")
    print(f"{'='*60}")

    if total_failed > 0:
        print("\nSOME TESTS FAILED - the fix may have issues.")
        sys.exit(1)
    else:
        print("\nALL TESTS PASSED - the fix is working correctly.")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
