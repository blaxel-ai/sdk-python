"""Sample: read the infrastructure failures the compute plane recorded on a sandbox.

The compute plane matches configured patterns in the microVM logs and signals them to
the control plane, which appends them to ``sandbox.errors`` (oldest first, bounded) and
moves the sandbox to FAILED for the fatal ones. Only a single-sandbox read returns the
array: listings never carry it.

The dev compute plane ships two fake patterns to produce entries on demand, both matched
in the microVM logs of the sandbox::

    echo blaxel-fake-vmm-error   # non-fatal, the sandbox keeps running
    echo blaxel-fake-vm-error    # fatal, moves the sandbox to FAILED

so a sandbox that never hit an incident legitimately reports an empty list.

Credentials are picked up automatically via blaxel.core autoload (local config / env).

Run:

    uv run python tests/manual/sandbox_errors.py

Env vars:
    NAME       sandbox to read (default: create a throwaway one)
    IMAGE      image for the created sandbox (default blaxel/base-image:latest)
    BL_REGION  region to create the sandbox in (optional)
    CLEANUP    delete a created sandbox at the end (default "true")
"""

import asyncio
import os
import uuid

from blaxel.core import SandboxInstance

NAME = os.environ.get("NAME")
IMAGE = os.environ.get("IMAGE", "blaxel/base-image:latest")
REGION = os.environ.get("BL_REGION")
CLEANUP = os.environ.get("CLEANUP", "true") != "false"


def log(msg: str) -> None:
    print(f"[errors] {msg}")


async def main() -> None:
    created = False
    if NAME:
        sandbox = await SandboxInstance.get(NAME)
    else:
        name = f"errors-{uuid.uuid4().hex[:8]}"
        log(f"creating sandbox {name}")
        sandbox = await SandboxInstance.create_if_not_exists(
            {
                "name": name,
                "image": IMAGE,
                **({"region": REGION} if REGION else {}),
            }
        )
        created = True

    log(f"sandbox {sandbox.metadata.name} status={sandbox.status}")

    # Always a list: empty when the sandbox never hit an infrastructure failure.
    errors = sandbox.errors
    log(f"{len(errors)} infrastructure error(s) recorded")
    for error in errors:
        log(
            f"  {error.time} {error.code} fatal={bool(error.fatal)} "
            f"instance={error.instance or '-'} {error.message or ''}".rstrip()
        )

    fatal = [error for error in errors if error.fatal]
    if fatal:
        # The last fatal entry is why the sandbox is FAILED, and its code is the same
        # one the gateway answers with (WORKLOAD_FAILED responses).
        log(f"sandbox failed on {fatal[-1].code}")

    # Listings drop the array, so never look for a failure reason there.
    page = await SandboxInstance.list(limit=1)
    if page.data:
        listed = page.data[0]
        log(f"listed {listed.metadata.name} carries errors: {bool(listed.errors)}")

    if created and CLEANUP:
        await SandboxInstance.delete(sandbox.metadata.name)


if __name__ == "__main__":
    asyncio.run(main())
