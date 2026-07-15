import asyncio
import random
import string

from blaxel.core.client.api.agents.list_agents import asyncio as list_agents
from blaxel.core.client.api.functions.list_functions import asyncio as list_functions
from blaxel.core.client.api.integrations.list_integration_connections import (
    asyncio as list_integration_connections,
)
from blaxel.core.client.api.jobs.list_jobs import asyncio as list_jobs
from blaxel.core.client.api.models.list_models import asyncio as list_models
from blaxel.core.client.api.policies.list_policies import asyncio as list_policies
from blaxel.core.client.client import client

suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
missing = f"missing-{suffix}"


async def main():
    checks = [
        ("agents", lambda: list_agents(client=client, external_id=missing, limit=1)),
        ("functions", lambda: list_functions(client=client, external_id=missing, limit=1)),
        (
            "integration_connections",
            lambda: list_integration_connections(client=client, external_id=missing),
        ),
        ("jobs", lambda: list_jobs(client=client, external_id=missing, limit=1)),
        ("models", lambda: list_models(client=client, external_id=missing, limit=1)),
        ("policies", lambda: list_policies(client=client, external_id=missing, limit=1)),
    ]
    for label, check in checks:
        result = await check()
        if result is None:
            raise AssertionError(f"{label} external_id list returned None")
        print(f"{label} external_id list filter smoke passed")


asyncio.run(main())
