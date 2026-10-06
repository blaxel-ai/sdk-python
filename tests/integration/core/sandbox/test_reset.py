"""Reset a sandbox to a fresh copy of its image."""

import time
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxAPIError, SandboxInstance, SyncSandboxInstance
from blaxel.core.volume import VolumeInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    unique_name,
    wait_for_sandbox_deletion,
)

BOOT_ID = "cat /proc/sys/kernel/random/boot_id"


async def run(sandbox: SandboxInstance, command: str) -> str:
    result = await sandbox.process.exec({"command": command, "wait_for_completion": True})
    return (result.logs or "").strip()


async def exists(sandbox: SandboxInstance, path: str) -> bool:
    try:
        await sandbox.fs.read(path)
        return True
    except Exception:
        return False


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxReset:
    """A reset takes the sandbox back to its image and keeps the rest of it."""

    sandboxes: list[str] = []
    volumes: list[str] = []

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        for name in TestSandboxReset.sandboxes:
            try:
                await SandboxInstance.delete(name)
                await wait_for_sandbox_deletion(name)
            except Exception:
                pass
        for name in TestSandboxReset.volumes:
            try:
                await VolumeInstance.delete(name)
            except Exception:
                pass
        TestSandboxReset.sandboxes.clear()
        TestSandboxReset.volumes.clear()

    async def test_gives_back_a_fresh_copy_of_the_image_and_keeps_the_rest(self):
        name = unique_name("reset")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "memory": 2048,
                "region": default_region,
                "envs": [{"name": "RESET_SECRET", "value": "kept-across-reset"}],
                "ports": [{"name": "web", "target": 3000, "protocol": "HTTP"}],
                "labels": {**default_labels, "team": "reset-test"},
            }
        )
        TestSandboxReset.sandboxes.append(name)

        # Everything a user could have done to the sandbox since it started.
        await sandbox.fs.write("/home/user/leftover.txt", "build artifact")
        await run(sandbox, "mkdir -p /tmp/leftover && echo x > /tmp/leftover/x")
        await sandbox.process.exec({"name": "leftover-proc", "command": "sleep 3600"})
        preview = await sandbox.previews.create(
            {"metadata": {"name": "reset-preview"}, "spec": {"port": 3000, "public": False}}
        )
        token = await preview.tokens.create(datetime.now(timezone.utc) + timedelta(hours=1))
        boot_before = await run(sandbox, BOOT_ID)
        before = await SandboxInstance.get(name)

        started = time.monotonic()
        result = await sandbox.reset()
        elapsed = time.monotonic() - started

        # Back to DEPLOYED, on the instance that was called, in seconds.
        assert result is sandbox
        assert sandbox.status == "DEPLOYED"
        assert elapsed < 45

        # A new instance from the image: another boot, nothing left behind.
        assert await run(sandbox, BOOT_ID) != boot_before
        assert not await exists(sandbox, "/home/user/leftover.txt")
        assert not await exists(sandbox, "/tmp/leftover/x")
        assert await run(sandbox, "ps aux | grep -c '[s]leep 3600' || true") == "0"

        # The same sandbox: record, spec, secret environment variable, previews.
        after = await SandboxInstance.get(name)
        assert after.metadata.created_at == before.metadata.created_at
        assert after.metadata.labels["team"] == "reset-test"
        assert after.spec.runtime.image == default_image
        assert after.spec.runtime.memory == 2048
        assert 3000 in [port.target for port in after.spec.runtime.ports]
        assert await run(after, 'printf "%s" "$RESET_SECRET"') == "kept-across-reset"
        previews = await after.previews.list()
        assert "reset-preview" in [p.name for p in previews]
        preview_after = next(p for p in previews if p.name == "reset-preview")
        assert token.value in [t.value for t in await preview_after.tokens.list()]

        # It keeps working afterwards, and resetting again works too.
        await after.fs.write("/home/user/after.txt", "ok")
        again = await SandboxInstance.reset(name)
        assert again.status == "DEPLOYED"
        assert not await exists(again, "/home/user/after.txt")

    async def test_keeps_an_attached_volume_and_its_data(self):
        volume_name = unique_name("reset-vol")
        name = unique_name("reset-volume")
        await VolumeInstance.create(
            {
                "name": volume_name,
                "size": 1024,
                "region": default_region,
                "labels": default_labels,
            }
        )
        TestSandboxReset.volumes.append(volume_name)
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "volumes": [{"name": volume_name, "mount_path": "/data", "read_only": False}],
                "labels": default_labels,
            }
        )
        TestSandboxReset.sandboxes.append(name)
        await run(sandbox, "echo persistent > /data/keep.txt")
        await sandbox.fs.write("/home/user/leftover.txt", "build artifact")

        await sandbox.reset()

        assert not await exists(sandbox, "/home/user/leftover.txt")
        assert await run(sandbox, "cat /data/keep.txt") == "persistent"
        assert [v.name for v in sandbox.spec.volumes] == [volume_name]
        # The volume is mounted for writing again.
        await run(sandbox, "echo second > /data/second.txt")
        assert await run(sandbox, "cat /data/second.txt") == "second"

    async def test_does_not_bring_a_deleted_sandbox_back_to_life(self):
        name = unique_name("reset-deleted")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
            }
        )
        TestSandboxReset.sandboxes.append(name)
        await SandboxInstance.delete(name)
        await wait_for_sandbox_deletion(name)

        with pytest.raises(SandboxAPIError) as raised:
            await SandboxInstance.reset(name)
        # Either the record is gone (404) or it is still there as TERMINATED/DELETING.
        assert raised.value.status_code == 404 or "cannot be reset" in str(raised.value)

        # Still not running after the refused call.
        try:
            status = str((await SandboxInstance.get(name)).status)
        except SandboxAPIError:
            status = "GONE"
        assert status in ("TERMINATED", "DELETING", "GONE")


class TestSyncSandboxReset:
    """The blocking client resets a sandbox the same way."""

    def test_gives_back_a_fresh_copy_of_the_image(self):
        name = unique_name("reset-sync")
        sandbox = SyncSandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "region": default_region,
                "envs": [{"name": "RESET_SECRET", "value": "kept-across-reset"}],
                "labels": default_labels,
            }
        )
        try:
            sandbox.fs.write("/home/user/leftover.txt", "build artifact")
            boot_before = sandbox.process.exec(
                {"command": BOOT_ID, "wait_for_completion": True}
            ).logs.strip()

            result = sandbox.reset()

            assert result is sandbox
            assert sandbox.status == "DEPLOYED"
            boot_after = sandbox.process.exec(
                {"command": BOOT_ID, "wait_for_completion": True}
            ).logs.strip()
            assert boot_after != boot_before
            with pytest.raises(Exception):
                sandbox.fs.read("/home/user/leftover.txt")
            secret = sandbox.process.exec(
                {"command": 'printf "%s" "$RESET_SECRET"', "wait_for_completion": True}
            ).logs.strip()
            assert secret == "kept-across-reset"
        finally:
            try:
                SyncSandboxInstance.delete(name)
            except Exception:
                pass
