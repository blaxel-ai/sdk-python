"""Tests for external_id list filters on remaining root resources."""

import pytest

from blaxel.core.client.api.agents import list_agents
from blaxel.core.client.api.functions import list_functions
from blaxel.core.client.api.integrations import list_integration_connections
from blaxel.core.client.api.jobs import list_jobs
from blaxel.core.client.api.models import list_models
from blaxel.core.client.api.policies import list_policies


@pytest.mark.parametrize(
    ("module", "url"),
    [
        (list_agents, "/agents"),
        (list_functions, "/functions"),
        (list_integration_connections, "/integrations/connections"),
        (list_jobs, "/jobs"),
        (list_models, "/models"),
        (list_policies, "/policies"),
    ],
)
def test_remaining_root_list_external_id_query_param(module, url):
    kwargs = module._get_kwargs(external_id="remaining-root-external-id")

    assert kwargs["url"] == url
    assert kwargs["params"]["externalId"] == "remaining-root-external-id"
