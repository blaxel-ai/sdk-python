import asyncio

import pytest
import pytest_asyncio

from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    unique_name,
    wait_for_sandbox_deployed,
)


@pytest.mark.asyncio(loop_scope="class")
class TestUpdateEnvs:
    """SandboxInstance.update_envs changes variables without recreating the sandbox."""

    created_sandboxes: list[str] = []

    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="class")
    async def cleanup(self):
        yield
        await asyncio.gather(
            *[SandboxInstance.delete(name) for name in TestUpdateEnvs.created_sandboxes],
            return_exceptions=True,
        )
        TestUpdateEnvs.created_sandboxes.clear()

    async def _echo(self, sandbox: SandboxInstance, names: list[str]) -> str:
        command = " ".join(f'echo "{name}=${{{name}:-unset}}";' for name in names)
        result = await sandbox.process.exec({"command": command, "wait_for_completion": True})
        return result.logs

    async def test_merge_remove_and_replace(self):
        name = unique_name("update-envs")
        sandbox = await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
                "envs": [
                    {"name": "KEEP", "value": "kept"},
                    {"name": "CHANGE", "value": "before"},
                    {"name": "DROP", "value": "dropped"},
                ],
            }
        )
        TestUpdateEnvs.created_sandboxes.append(name)
        updated = await SandboxInstance.update_envs(
            name, {"CHANGE": "after", "DROP": None, "ADDED": "new"}
        )
        # The API masks values in its responses, so only names can be checked here.
        assert [env.name for env in updated.spec.runtime.envs] == ["KEEP", "CHANGE", "ADDED"]

        # The new environment reaches the sandbox a few seconds after the update.
        assert await wait_for_sandbox_deployed(name)
        sandbox = await SandboxInstance.get(name)
        logs = await self._echo(sandbox, ["KEEP", "CHANGE", "DROP", "ADDED"])
        assert "KEEP=kept" in logs
        assert "CHANGE=after" in logs
        assert "DROP=unset" in logs
        assert "ADDED=new" in logs

        replaced = await SandboxInstance.update_envs(name, {"ONLY": "one"}, replace=True)
        assert [env.name for env in replaced.spec.runtime.envs] == ["ONLY"]
        assert await wait_for_sandbox_deployed(name)
        logs = await self._echo(await SandboxInstance.get(name), ["ONLY", "KEEP"])
        assert "ONLY=one" in logs
        assert "KEEP=unset" in logs

    async def test_list_form_keeps_secret_flag(self):
        name = unique_name("update-envs-secret")
        await SandboxInstance.create(
            {
                "name": name,
                "image": default_image,
                "labels": default_labels,
                "envs": [{"name": "PLAIN", "value": "plain"}],
            }
        )
        TestUpdateEnvs.created_sandboxes.append(name)

        updated = await SandboxInstance.update_envs(
            name, [{"name": "API_KEY", "value": "s3cr3t-value", "secret": True}]
        )
        secrets = {env.name: env.secret for env in updated.spec.runtime.envs}
        assert secrets["API_KEY"] is True
        assert "PLAIN" in secrets

        assert await wait_for_sandbox_deployed(name)
        logs = await self._echo(await SandboxInstance.get(name), ["API_KEY", "PLAIN"])
        assert "API_KEY=s3cr3t-value" in logs
        assert "PLAIN=plain" in logs
