"""Probe for destination-scoped workspace secrets (controlplane#5802)."""

from blaxel.core.client.client import client

from .utils import unique_name


def destinations_supported() -> bool:
    """Workspace secrets are behind the "workspace-secrets" feature flag (403 when off, 404 on
    environments that predate controlplane#5736), and environments that predate
    controlplane#5802 accept but silently drop `destinations` (and the generated `Secret`
    model then fails to parse their responses). Probe with a throwaway secret and only run
    the secrets tests when the API echoes the destinations back."""
    http = client.get_httpx_client()
    name = unique_name("sdk-test-secret-probe").replace(".", "-")
    response = http.post(
        "/secrets", json={"name": name, "value": "probe", "destinations": ["api.stripe.com"]}
    )
    if response.status_code != 200:
        return False
    http.delete(f"/secrets/{name}")
    return isinstance(response.json().get("destinations"), list)
