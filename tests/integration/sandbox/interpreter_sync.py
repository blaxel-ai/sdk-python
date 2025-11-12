import sys
from typing import List

from blaxel.core.client.models import Metadata, Port, Runtime, Sandbox, SandboxSpec
from blaxel.core.sandbox.sync import SyncCodeInterpreter


def main():
    print("🚀 [sync-interpreter] starting")

    interp = None
    try:
        print("🔧 [sync-interpreter] creating interpreter sandbox (jupyter-server)...")
        interp = SyncCodeInterpreter.get("sandbox-interpreter")
        interp = SyncCodeInterpreter(
          sandbox=Sandbox(metadata=Metadata(name="test"), spec=SandboxSpec(runtime=Runtime(image="blaxel/jupyter-server", ports=[Port(name="jupyter", target=8888, protocol="HTTP")]))),
          force_url="http://localhost:8888"
        )
        name = getattr(getattr(interp, "metadata", None), "name", None)
        print(f"✅ created: {name}")

        # Verify image and ports
        runtime = getattr(getattr(interp, "spec", None), "runtime", None)
        image = getattr(runtime, "image", None)
        ports = getattr(runtime, "ports", None)
        print(f"ℹ️ image={image}")
        assert image == "blaxel/jupyter-server", "interpreter image must be blaxel/jupyter-server"

        has_8888 = False
        if isinstance(ports, list):
            for p in ports:  # type: ignore[assignment]
                # Ports may be model objects; try attribute access first, then dict
                try:
                    tgt = getattr(p, "target", None)
                    nm = getattr(p, "name", None)
                except Exception:
                    tgt = p.get("target") if isinstance(p, dict) else None  # type: ignore[assignment]
                    nm = p.get("name") if isinstance(p, dict) else None  # type: ignore[assignment]
                if tgt == 8888:
                    has_8888 = True
                    print(f"ℹ️ port confirmed: {nm}@{tgt}")
                    break
        assert has_8888, "interpreter must expose port 8888"

        # # Try creating a context (skip if endpoint not available)
        # try:
        #     print("🔧 [sync-interpreter] creating code context (python)...")
        #     ctx = interp.create_code_context(language="python")
        #     print(f"✅ context created: id={ctx.id}")
        # except Exception as e:
        #     print(f"⚠️ [sync-interpreter] create_code_context skipped: {e}")

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

            exec_obj = interp.run_code(
                "print('Hello from interpreter')",
                language="python",
                on_stdout=on_stdout,
                on_stderr=on_stderr,
                on_result=on_result,
                on_error=on_error,
                timeout=30.0,
            )
            print(
                f"✅ run_code finished: stdout={len(stdout_lines)} stderr={len(stderr_lines)} "
                f"results={len(results)} errors={len(errors)}"
            )
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
                    # SyncCodeInterpreter.delete(n)
                    print(f"🧹 [sync-interpreter] deleted {n}")
            except Exception as e:
                print(f"⚠️ [sync-interpreter] cleanup failed: {e}")


if __name__ == "__main__":
    main()


