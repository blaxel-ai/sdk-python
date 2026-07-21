"""Tests for the sandbox network config models (firewall + proxy body)."""

from blaxel.core.client.models import FirewallConfig, ProxyConfig, SandboxNetwork


def test_firewall_config_round_trip():
    """FirewallConfig serializes rulesets and parses them back."""
    fw = FirewallConfig(rulesets=["proxy", "dedicated-ip"])
    assert fw.to_dict() == {"rulesets": ["proxy", "dedicated-ip"]}

    parsed = FirewallConfig.from_dict({"rulesets": ["default"]})
    assert parsed.rulesets == ["default"]


def test_firewall_config_empty():
    """An empty FirewallConfig omits rulesets and from_dict of empty is None."""
    assert FirewallConfig().to_dict() == {}
    assert FirewallConfig.from_dict({}) is None


def test_proxy_config_allowed_and_forbidden_domains():
    """ProxyConfig exposes allowed/forbidden domains with camelCase keys."""
    proxy = ProxyConfig(
        allowed_domains=["api.stripe.com", "*.s3.amazonaws.com"],
        forbidden_domains=["*.malware.com"],
        bypass=["*.internal"],
    )

    serialized = proxy.to_dict()
    assert serialized["allowedDomains"] == ["api.stripe.com", "*.s3.amazonaws.com"]
    assert serialized["forbiddenDomains"] == ["*.malware.com"]
    assert serialized["bypass"] == ["*.internal"]

    parsed = ProxyConfig.from_dict(serialized)
    assert parsed.allowed_domains == ["api.stripe.com", "*.s3.amazonaws.com"]
    assert parsed.forbidden_domains == ["*.malware.com"]
    assert parsed.bypass == ["*.internal"]


def test_sandbox_network_firewall_and_subnet():
    """SandboxNetwork carries firewall + subnet and round-trips them."""
    payload = {
        "firewall": {"rulesets": ["proxy"]},
        "subnet": "sn-1",
        "proxy": {
            "allowedDomains": ["api.stripe.com"],
            "forbiddenDomains": ["*.evil.com"],
        },
    }

    network = SandboxNetwork.from_dict(payload)
    assert isinstance(network.firewall, FirewallConfig)
    assert network.firewall.rulesets == ["proxy"]
    assert network.subnet == "sn-1"
    assert isinstance(network.proxy, ProxyConfig)
    assert network.proxy.allowed_domains == ["api.stripe.com"]
    assert network.proxy.forbidden_domains == ["*.evil.com"]

    serialized = network.to_dict()
    assert serialized["firewall"] == {"rulesets": ["proxy"]}
    assert serialized["subnet"] == "sn-1"
    assert serialized["proxy"]["allowedDomains"] == ["api.stripe.com"]
    assert serialized["proxy"]["forbiddenDomains"] == ["*.evil.com"]


def test_sandbox_network_firewall_enables_proxy_ruleset():
    """The common firewall: {rulesets: ["proxy"]} shape is constructible from objects."""
    network = SandboxNetwork(firewall=FirewallConfig(rulesets=["proxy"]))
    assert network.to_dict() == {"firewall": {"rulesets": ["proxy"]}}
