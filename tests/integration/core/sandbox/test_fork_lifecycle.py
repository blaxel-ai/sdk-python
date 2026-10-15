import pytest
import pytest_asyncio

from blaxel.core.client.models import SandboxLifecycle
from blaxel.core.sandbox import SandboxInstance
from tests.helpers import (
    default_image,
    default_labels,
    default_region,
    skip_unless_generation_mk31,
    unique_name,
)


def policies(lifecycle: SandboxLifecycle | None) -> list[dict[str, str]]:
    policies = (lifecycle.to_dict() if lifecycle else {}).get("expirationPolicies", [])
    return [{"type": policy["type"], "value": policy["value"]} for policy in policies]


@pytest.mark.asyncio(loop_scope="class")
class TestSandboxForkLifecycle:
    source_name = unique_name("fork-lc-src")
    inherited_name = unique_name("fork-lc-inh")
    requested_name = unique_name("fork-lc-req")

    @pytest_asyncio.fixture(autouse=True)
    async def cleanup(self):
        yield
        for name in (
            TestSandboxForkLifecycle.requested_name,
            TestSandboxForkLifecycle.inherited_name,
            TestSandboxForkLifecycle.source_name,
        ):
            try:
                await SandboxInstance.delete(name)
            except Exception:
                pass

    async def test_inherits_the_sources_expiration_unless_the_fork_names_its_own(self):
        await skip_unless_generation_mk31("forks")

        source = await SandboxInstance.create(
            {
                "name": TestSandboxForkLifecycle.source_name,
                "image": default_image,
                "region": default_region,
                "labels": default_labels,
                "ttl": "3h",
                "lifecycle": {
                    "expirationPolicies": [
                        {"type": "ttl-max-age", "value": "2h", "action": "delete"},
                        {"type": "ttl-idle", "value": "1h", "action": "delete"},
                    ]
                },
            }
        )

        await source.fork(TestSandboxForkLifecycle.inherited_name)
        inherited = await SandboxInstance.get(TestSandboxForkLifecycle.inherited_name)
        assert policies(inherited.spec.lifecycle) == [
            {"type": "ttl-max-age", "value": "2h"},
            {"type": "ttl-idle", "value": "1h"},
        ]
        assert inherited.spec.runtime.ttl == "3h"

        await source.fork(
            TestSandboxForkLifecycle.requested_name,
            lifecycle={
                "expirationPolicies": [
                    {"type": "ttl-max-age", "value": "45m", "action": "delete"},
                ]
            },
        )
        requested = await SandboxInstance.get(TestSandboxForkLifecycle.requested_name)
        assert policies(requested.spec.lifecycle) == [{"type": "ttl-max-age", "value": "45m"}]
