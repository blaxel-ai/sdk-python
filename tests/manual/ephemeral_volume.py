"""Sample: create a sandbox with an ephemeral (disk-backed scratch) volume.

Ephemeral volumes are created together with the sandbox on the mk3.1 (Firecracker)
generation and live only for the sandbox's lifetime. Unlike persistent volumes, there
is no Volume resource to create beforehand: you just declare the attachment with
``type="ephemeral"`` and a ``size_mb``.

This script intentionally does NOT delete the sandbox, so you can inspect the mounted
scratch disk manually (e.g. via ``df -h`` / writing files under the mount path). Delete
it yourself when done:

    python -c "import asyncio; from blaxel.core import SandboxInstance; asyncio.run(SandboxInstance.delete('<name>'))"

Requires the ``generation_mk31`` feature flag enabled on the workspace. Credentials are
picked up automatically via blaxel.core autoload (local config / env), so BL_WORKSPACE /
BL_API_KEY are not required here.

Run:

    uv run python tests/manual/ephemeral_volume.py

Env vars:
    NAME          sandbox name (default: ephemeral-<random>)
    VOLUME        ephemeral volume name (default: scratch)
    SIZE_MB       ephemeral volume size in MB (default 1024)
    MOUNT_PATH    where the volume is mounted (default /scratch)
    BL_REGION     region to create the sandbox in (optional)
    IMAGE         sandbox image (default blaxel/base-image:latest)
"""

import asyncio
import os
import sys
import time
import uuid

from blaxel.core import SandboxInstance

VOLUME = os.environ.get("VOLUME", "scratch")
SIZE_MB = int(os.environ.get("SIZE_MB", "1024"))
MOUNT_PATH = os.environ.get("MOUNT_PATH", "/scratch")
REGION = os.environ.get("BL_REGION")
IMAGE = os.environ.get("IMAGE", "blaxel/base-image:latest")
LABELS = {"env": "manual-test", "created-by": "ephemeral-volume"}

EXEC_TIMEOUT_S = 600


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def log(msg: str) -> None:
    print(f"[ephemeral] {msg}")


async def run(sandbox: SandboxInstance, command: str, label: str) -> str:
    result = await sandbox.process.exec(
        {
            "command": command,
            "wait_for_completion": True,
            "timeout": EXEC_TIMEOUT_S,
        }
    )
    if result.exit_code != 0:
        raise RuntimeError(f"{label} failed (exit {result.exit_code}):\n{result.logs or ''}")
    return (result.logs or "").strip()


async def main() -> None:
    name = os.environ.get("NAME") or unique_name("ephemeral")
    t0 = time.time()

    log(f"creating sandbox {name} with ephemeral volume {VOLUME} ({SIZE_MB} MB) at {MOUNT_PATH}")
    sandbox = await SandboxInstance.create(
        {
            "name": name,
            "image": IMAGE,
            **({"region": REGION} if REGION else {}),
            "labels": LABELS,
            "volumes": [
                {
                    "name": VOLUME,
                    "mount_path": MOUNT_PATH,
                    "type": "ephemeral",
                    "size_mb": SIZE_MB,
                },
            ],
        }
    )

    log(f"sandbox {name} is ready — checking the mounted scratch disk")

    df_out = await run(sandbox, f"df -h {MOUNT_PATH} || df -h", "df")
    log(f"df:\n{df_out}")

    await run(
        sandbox,
        f"echo 'hello from ephemeral volume' > {MOUNT_PATH}/hello.txt && sync",
        "write",
    )
    cat_out = await run(sandbox, f"cat {MOUNT_PATH}/hello.txt", "read")
    log(f"wrote and read back: {cat_out}")

    log(f"done in {time.time() - t0:.1f}s")
    log(f"sandbox {name} was left running for manual inspection — remember to delete it when done.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:  # noqa: BLE001
        print(f"Fatal error: {err}", file=sys.stderr)
        sys.exit(1)
