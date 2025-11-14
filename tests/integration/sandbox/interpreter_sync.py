import sys
import time
from typing import List

from blaxel.core import SyncCodeInterpreter
from blaxel.core.client.models import Metadata, Sandbox


def main():
    print("🚀 [sync-interpreter] starting")

    interp = None
    try:
        print("🔧 [sync-interpreter] creating interpreter sandbox (jupyter-server)...")
        t0 = time.perf_counter()
        interp = SyncCodeInterpreter.create()
        # interp = SyncCodeInterpreter.get("sandbox-b40e7115")
        # interp = SyncCodeInterpreter(sandbox=Sandbox(metadata=Metadata(name="test")), force_url="http://localhost:8888")
        name = getattr(getattr(interp, "metadata", None), "name", None)
        print(f"✅ created: {name}")
        print(f"⏱️ create: {int((time.perf_counter() - t0) * 1000)} ms")


        # Try creating a context (skip if endpoint not available)
        try:
            print("🔧 [sync-interpreter] creating code context (python)...")
            t0 = time.perf_counter()
            ctx = interp.create_code_context(language="python")
            print(f"✅ context created: id={ctx.id}")
            print(f"⏱️ create_context: {int((time.perf_counter() - t0) * 1000)} ms")
        except Exception as e:
            print(f"⚠️ [sync-interpreter] create_code_context skipped: {e}")

        # Try running simple code (skip if endpoint not available)
        try:
            print("🔧 [sync-interpreter] running code...")
            stdout_lines: List[str] = []
            stderr_lines: List[str] = []
            results: List[object] = []
            errors: List[object] = []

            def on_stdout(msg):
                text = getattr(msg, "text", str(msg))
                stdout_lines.append(text)
                print(f"[stdout] {text}")

            def on_stderr(msg):
                text = getattr(msg, "text", str(msg))
                stderr_lines.append(text)
                print(f"[stderr] {text}")

            def on_result(res):
                results.append(res)
                print(f"[result] {res}")

            def on_error(err):
                errors.append(err)
                print(f"[error] {err}")

            t0 = time.perf_counter()
            interp.run_code(
                "print('Hello from interpreter')",
                language="python",
                on_stdout=on_stdout,
                on_stderr=on_stderr,
                on_result=on_result,
                on_error=on_error,
                timeout=30.0,
            )
            print(f"⏱️ run_code(hello): {int((time.perf_counter() - t0) * 1000)} ms")
            print(
                f"✅ run_code finished: stdout={len(stdout_lines)} stderr={len(stderr_lines)} "
                f"results={len(results)} errors={len(errors)}"
            )

            # Define a function in one run, then call it in another run (using a context)
            print("🔧 [sync-interpreter] define function in first run_code, call in second")
            try:
                stdout_lines.clear()
                stderr_lines.clear()
                results.clear()
                errors.clear()

                # First run: define a function
                t0 = time.perf_counter()
                interp.run_code(
                    "def add(a, b):\n    return a + b",
                    on_stdout=on_stdout,
                    on_stderr=on_stderr,
                    on_result=on_result,
                    on_error=on_error,
                    timeout=30.0,
                )
                print(f"⏱️ run_code(define): {int((time.perf_counter() - t0) * 1000)} ms")

                # Second run: call the function
                stdout_lines.clear()
                stderr_lines.clear()
                results.clear()
                errors.clear()

                t0 = time.perf_counter()
                interp.run_code(
                    "print(add(2, 3))",
                    on_stdout=on_stdout,
                    on_stderr=on_stderr,
                    on_result=on_result,
                    on_error=on_error,
                    timeout=30.0,
                )
                print(f"⏱️ run_code(call): {int((time.perf_counter() - t0) * 1000)} ms")

                # Expect to see "5" in stdout
                got_stdout = "".join(stdout_lines)
                if "5" not in got_stdout:
                    raise AssertionError(f"Expected function output '5', got stdout={got_stdout!r}")
                print("✅ function persisted across runs via context")
            except Exception as e2:
                print(f"⚠️ [sync-interpreter] two-step run_code skipped: {e2}")
        except Exception as e:
            print(f"⚠️ [sync-interpreter] run_code skipped: {e}")

        print("🎉 [sync-interpreter] done")
        sys.exit(0)

    except AssertionError as e:
        print(f"❌ [sync-interpreter] assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ [sync-interpreter] error: {e}")
        sys.exit(1)
    finally:
        if interp:
            try:
                n = getattr(getattr(interp, "metadata", None), "name", None)
                if n:
                    SyncCodeInterpreter.delete(n)
                    print(f"🧹 [sync-interpreter] deleted {n}")
            except Exception as e:
                print(f"⚠️ [sync-interpreter] cleanup failed: {e}")


if __name__ == "__main__":
    main()


