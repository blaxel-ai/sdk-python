"""Live typed-error contract, including sync/async parity and resource cleanup."""

import pytest
import pytest_asyncio

from blaxel.core import (
    BlaxelError,
    SandboxAPIError,
    SandboxInstance,
    SyncSandboxInstance,
    is_blaxel_error,
)
from tests.helpers import default_image, default_labels, default_region, unique_name


@pytest.mark.asyncio(loop_scope="class")
class TestTypedErrors:
    names: set[str]

    @pytest_asyncio.fixture(scope="class", loop_scope="class", autouse=True)
    async def cleanup(self):
        type(self).names = set()
        yield
        for name in self.names:
            try:
                sandbox = await SandboxInstance.get(name)
                await sandbox.delete()
            except SandboxAPIError as error:
                if error.status != 404:
                    raise

    @staticmethod
    def check_response(error: BlaxelError, status: int) -> None:
        assert is_blaxel_error(error)
        assert error.status == status
        assert error.response is not None
        assert error.response.status_code == status
        with pytest.raises(RuntimeError, match="request"):
            _ = error.response.request
        assert isinstance(error.body, dict)
        assert error.message == str(error)
        print(f"live error: status={error.status} code={error.code} request_id={error.request_id}")

    @pytest.mark.parametrize("sync", [False, True])
    async def test_missing_sandbox(self, sync):
        name = unique_name("typed-errors-missing")
        with pytest.raises(SandboxAPIError) as caught:
            if sync:
                SyncSandboxInstance.get(name)
            else:
                await SandboxInstance.get(name)
        self.check_response(caught.value, 404)
        # The generic endpoint keeps the legacy string code and numeric wire code.
        assert caught.value.body["code"] == 404

    @pytest.mark.parametrize("sync", [False, True])
    async def test_invalid_image(self, sync):
        name = unique_name("typed-errors-image")
        self.names.add(name)
        config = {
            "name": name,
            "image": "this-image-does-not-exist-pm2046",
            "region": default_region,
            "labels": default_labels,
        }
        with pytest.raises(SandboxAPIError) as caught:
            if sync:
                SyncSandboxInstance.create(config, timeout=20)
            else:
                await SandboxInstance.create(config, timeout=20)
        self.check_response(caught.value, 400)
        assert is_blaxel_error(caught.value, ["INVALID_IMAGE", "IMAGE_NOT_FOUND"])

    @pytest.mark.parametrize("sync", [False, True])
    async def test_duplicate_sandbox_name(self, sync):
        name = unique_name("typed-errors-duplicate")
        self.names.add(name)
        config = {
            "name": name,
            "image": default_image,
            "region": default_region,
            "labels": default_labels,
            "ttl": "5m",
        }
        await SandboxInstance.create(config, timeout=20)
        with pytest.raises(SandboxAPIError) as caught:
            if sync:
                SyncSandboxInstance.create(config, timeout=20)
            else:
                await SandboxInstance.create(config, timeout=20)
        self.check_response(caught.value, 409)
        assert is_blaxel_error(caught.value, "SANDBOX_ALREADY_EXISTS")
