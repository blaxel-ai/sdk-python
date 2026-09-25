"""Manual end-to-end test for forking a sandbox with new environment variables.

``sandbox.fork(name, envs=[...])`` sends the variables the fork should run with
on top of the ones the source has: a variable the source already carries takes
the value given here, one it does not is added, and every other variable of the
source is kept. The fork boots with that environment already applied — no
second update call.

Flow:
    1. Create a source sandbox carrying MODE=source and SOURCE_ONLY=1.
    2. Read both back from a process inside it.
    3. Fork it with envs = [MODE=fork, FORK_ONLY=1].
    4. Assert a process in the fork sees MODE=fork (replaced),
       SOURCE_ONLY=1 (inherited) and FORK_ONLY=1 (added).
    5. Assert the source still sees MODE=source and no FORK_ONLY.
    6. Clean up both sandboxes (KEEP=1 to inspect them instead).

This lives under tests/manual because it creates two real sandboxes and forks
between them, well past the 1-minute budget of the integration suite. It also
needs the backend halves deployed to the environment it runs against.

Credentials are picked up automatically via blaxel.core autoload (local
``bl login`` config / env), so BL_WORKSPACE / BL_API_KEY are not required here.
BL_ENV=dev targets api.blaxel.dev.

Install and run (``uv sync`` without extras: the framework extras conflict with
each other and this only needs blaxel.core):

    uv sync
    uv run python tests/manual/fork_with_environment.py

Env vars:
    NAME       source sandbox name (default: fork-env-<random>)
    IMAGE      sandbox image (default blaxel/base-image:latest)
    BL_REGION  region to create the source sandbox in (optional)
    KEEP       set to 1 to keep both sandboxes for inspection
"""

import asyncio
import os
import sys
import time
import uuid

from blaxel.core import SandboxInstance
from blaxel.core.client.models import Env

IMAGE = os.environ.get("IMAGE", "blaxel/base-image:latest")
REGION = os.environ.get("BL_REGION")
KEEP = os.environ.get("KEEP") == "1"
LABELS = {"env": "manual-test", "created-by": "fork-with-environment"}
WATCHED = ["MODE", "SOURCE_ONLY", "FORK_ONLY"]

t0 = time.time()


def unique_name(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def log(msg: str) -> None:
    print(f"[{time.time() - t0:.1f}s] {msg}")


async def read_env(sandbox: SandboxInstance, names: list[str]) -> dict[str, str]:
    """Read the environment a freshly spawned process in the sandbox inherits."""
    script = "; ".join(f'printf "{name}=%s\\n" "${name}"' for name in names)
    result = await sandbox.process.exec(
        {"command": f"sh -c '{script}'", "wait_for_completion": True}
    )
    env: dict[str, str] = {}
    for line in (result.logs or "").split("\n"):
        separator = line.find("=")
        if separator > 0:
            env[line[:separator]] = line[separator + 1 :].strip()
    return env


async def read_env_when_up(
    sandbox: SandboxInstance, names: list[str], retries: int, delay_s: float
) -> dict[str, str]:
    """Retry until the fork answers: a fork returns before its guest has resumed."""
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            return await read_env(sandbox, names)
        except Exception as err:  # noqa: BLE001
            last_error = err
            await asyncio.sleep(delay_s)
    raise RuntimeError(f"{sandbox.metadata.name} never answered: {last_error}")


def assert_env(label: str, env: dict[str, str], expected: dict[str, str]) -> None:
    for name, value in expected.items():
        if env.get(name, "") != value:
            raise AssertionError(f"{label}: expected {name}={value!r}, got {env.get(name, '')!r}")
    print(f"  {label} ✔ {expected}")


async def main() -> None:
    source_name = os.environ.get("NAME") or unique_name("fork-env")
    fork_name = f"{source_name}-fork"
    created: list[str] = []

    try:
        log(f"creating source sandbox {source_name} with MODE=source SOURCE_ONLY=1")
        source = await SandboxInstance.create(
            {
                "name": source_name,
                "image": IMAGE,
                "memory": 2048,
                "labels": LABELS,
                **({"region": REGION} if REGION else {}),
                "envs": [
                    {"name": "MODE", "value": "source"},
                    {"name": "SOURCE_ONLY", "value": "1"},
                ],
            }
        )
        created.append(source_name)
        assert_env(
            "source before fork",
            await read_env_when_up(source, WATCHED, retries=15, delay_s=2),
            {"MODE": "source", "SOURCE_ONLY": "1", "FORK_ONLY": ""},
        )

        log(f"forking {source_name} -> {fork_name} with MODE=fork FORK_ONLY=1")
        forked = await source.fork(
            fork_name,
            envs=[
                Env(name="MODE", value="fork"),
                Env(name="FORK_ONLY", value="1"),
            ],
        )
        created.append(fork_name)
        log(f"forked into {forked.type_}: {forked.name}")

        fork = await SandboxInstance.get(fork_name)
        # Printed before the guest is read: it tells apart what the control
        # plane recorded from what the guest actually runs with.
        envs = fork.spec.runtime.envs if fork.spec and fork.spec.runtime else []
        print(f"  fork spec.runtime.envs: {envs}")
        assert_env(
            "fork",
            await read_env_when_up(fork, WATCHED, retries=30, delay_s=2),
            {"MODE": "fork", "SOURCE_ONLY": "1", "FORK_ONLY": "1"},
        )

        # The fork carries its own environment; the source is left as it was.
        assert_env(
            "source after fork",
            await read_env(source, WATCHED),
            {"MODE": "source", "SOURCE_ONLY": "1", "FORK_ONLY": ""},
        )

        print(
            "\n✅ Fork with new environment variables: replaced, inherited and added all verified."
        )
    finally:
        if KEEP:
            print(f"\n🔍 KEEP=1, leaving {', '.join(created)} in place")
        else:
            print("\n🧹 Cleaning up...")
            for name in created:
                try:
                    await SandboxInstance.delete(name)
                    print(f"  deleted sandbox {name}")
                except Exception as err:  # noqa: BLE001
                    print(f"  failed to delete {name}: {err}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:  # noqa: BLE001
        print(f"Fatal error: {err}", file=sys.stderr)
        sys.exit(1)
