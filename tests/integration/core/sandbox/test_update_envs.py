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

    async def _echo(self, name: str, expected: dict[str, str]) -> str:
        """Read ``expected``'s variables in a new process until they all match.

        The status can still read ``DEPLOYED`` from before the update when the
        polling starts, so the values themselves are what is waited for.
        """
        command = " ".join(f'echo "{var}=${{{var}:-unset}}";' for var in expected)
        lines = [f"{var}={value}" for var, value in expected.items()]
        logs = ""
        for _ in range(30):
            if await wait_for_sandbox_deployed(name):
                sandbox = await SandboxInstance.get(name)
                result = await sandbox.process.exec(
                    {"command": command, "wait_for_completion": True}
                )
                logs = result.logs or ""
                if all(line in logs.splitlines() for line in lines):
                    return logs
            await asyncio.sleep(1)
        return logs

    async def test_merge_remove_and_replace(self):
        name = unique_name("update-envs")
        await SandboxInstance.create(
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
        expected = {"KEEP": "kept", "CHANGE": "after", "DROP": "unset", "ADDED": "new"}
        logs = await self._echo(name, expected)
        for var, value in expected.items():
            assert f"{var}={value}" in logs

        replaced = await SandboxInstance.update_envs(name, {"ONLY": "one"}, replace=True)
        assert [env.name for env in replaced.spec.runtime.envs] == ["ONLY"]
        logs = await self._echo(name, {"ONLY": "one", "KEEP": "unset"})
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

        logs = await self._echo(name, {"API_KEY": "s3cr3t-value", "PLAIN": "plain"})
        assert "API_KEY=s3cr3t-value" in logs
        assert "PLAIN=plain" in logs
