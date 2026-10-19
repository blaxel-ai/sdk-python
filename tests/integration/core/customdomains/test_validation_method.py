"""Tests for the certificate validation method of custom domains (spec.validationMethod).

They create real custom domains in the tested workspace, so they are opt-in:
set RUN_CUSTOM_DOMAIN_TESTS=1 to run them. The names are unique subdomains of
example.com: nothing is ever verified, so no DNS record is needed.
"""

import logging
import os

import pytest

from blaxel.core.client.api.customdomains.create_custom_domain import (
    asyncio as create_custom_domain,
)
from blaxel.core.client.api.customdomains.get_custom_domain import (
    asyncio as get_custom_domain,
)
from blaxel.core.client.api.customdomains.update_custom_domain import (
    asyncio_detailed as update_custom_domain_detailed,
)
from blaxel.core.client.client import client
from blaxel.core.client.errors import UnexpectedStatus
from blaxel.core.client.models import (
    CustomDomain,
    CustomDomainMetadata,
    CustomDomainSpec,
    CustomDomainSpecDomainType,
    CustomDomainSpecValidationMethod,
    MetadataLabels,
)
from blaxel.core.client.types import UNSET, Unset
from tests.helpers import default_labels, unique_name

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("RUN_CUSTOM_DOMAIN_TESTS"),
        reason="creates custom domains; set RUN_CUSTOM_DOMAIN_TESTS=1 to enable",
    ),
    pytest.mark.asyncio(loop_scope="module"),
]

ACM_VALIDATION_SUFFIX = ".acm-validations.aws"


def _domain_name(prefix: str) -> str:
    return f"{unique_name(prefix)}.example.com"


def _custom_domain(
    name: str,
    domain_type: CustomDomainSpecDomainType = CustomDomainSpecDomainType.APPLICATIONS,
    validation_method: CustomDomainSpecValidationMethod | Unset = UNSET,
) -> CustomDomain:
    """Build a custom domain body; validation_method is omitted from the request when UNSET."""
    return CustomDomain(
        metadata=CustomDomainMetadata(name=name, labels=MetadataLabels.from_dict(default_labels)),
        spec=CustomDomainSpec(domain_type=domain_type, validation_method=validation_method),
    )


def _track(created_domains: list[str], body: CustomDomain) -> None:
    name = body.metadata.name
    assert isinstance(name, str)
    created_domains.append(name)


async def _create(created_domains: list[str], body: CustomDomain) -> CustomDomain:
    _track(created_domains, body)
    domain = await create_custom_domain(client=client, body=body)
    assert isinstance(domain, CustomDomain)
    return domain


async def _assert_create_rejected(
    created_domains: list[str], body: CustomDomain, status: int
) -> UnexpectedStatus:
    _track(created_domains, body)
    with pytest.raises(UnexpectedStatus) as exc_info:
        await create_custom_domain(client=client, body=body)
    assert exc_info.value.status_code == status, exc_info.value.content
    return exc_info.value


def _cname_records(domain: CustomDomain) -> dict[str, str]:
    # The API returns a name -> target map even though the spec types it as a string.
    records = domain.spec.cname_records
    assert isinstance(records, dict), records
    return records


async def test_omitted_validation_method_defaults_to_dns(created_domains):
    name = _domain_name("cd-default")
    body = _custom_domain(name)
    assert "validationMethod" not in body.to_dict()["spec"]

    created = await _create(created_domains, body)
    assert created.spec.validation_method == CustomDomainSpecValidationMethod.DNS

    fetched = await get_custom_domain(name, client=client)
    assert isinstance(fetched, CustomDomain)
    assert fetched.spec.validation_method == CustomDomainSpecValidationMethod.DNS


async def test_http_validation_on_application_domain(created_domains):
    """Succeeds when the workspace has custom-domain-http-validation, 403 otherwise."""
    name = _domain_name("cd-http")
    body = _custom_domain(name, validation_method=CustomDomainSpecValidationMethod.HTTP)
    created_domains.append(name)
    try:
        created = await create_custom_domain(client=client, body=body)
    except UnexpectedStatus as e:
        assert e.status_code == 403, e.content
        logger.warning("http validation is not enabled for this workspace: got 403")
        return

    logger.warning("http validation is enabled for this workspace: domain created")
    assert isinstance(created, CustomDomain)
    assert created.spec.validation_method == CustomDomainSpecValidationMethod.HTTP

    fetched = await get_custom_domain(name, client=client)
    assert isinstance(fetched, CustomDomain)
    assert fetched.spec.validation_method == CustomDomainSpecValidationMethod.HTTP
    records = _cname_records(fetched)
    assert name in records
    assert not any(
        record_name.rstrip(".").endswith(ACM_VALIDATION_SUFFIX)
        or target.rstrip(".").endswith(ACM_VALIDATION_SUFFIX)
        for record_name, target in records.items()
    ), records


async def test_http_validation_rejected_on_preview_domain(created_domains):
    body = _custom_domain(
        _domain_name("cd-prev"),
        domain_type=CustomDomainSpecDomainType.PREVIEWS,
        validation_method=CustomDomainSpecValidationMethod.HTTP,
    )
    await _assert_create_rejected(created_domains, body, 400)


async def test_http_validation_rejected_with_wildcard_san(created_domains):
    name = _domain_name("cd-wild")
    body = _custom_domain(name, validation_method=CustomDomainSpecValidationMethod.HTTP)
    # The spec types SANs as objects while the API takes plain strings, so send them raw.
    body.spec["subjectAlternativeNames"] = [f"*.{name}"]
    await _assert_create_rejected(created_domains, body, 400)


async def test_unknown_validation_method_rejected(created_domains):
    body = _custom_domain(_domain_name("cd-bogus"))
    # The generated enum refuses unknown values, so send it raw.
    body.spec["validationMethod"] = "bogus"
    await _assert_create_rejected(created_domains, body, 400)


async def test_validation_method_is_immutable_on_update(created_domains):
    """Changing the method on update is accepted (200) but the stored value is kept."""
    name = _domain_name("cd-immut")
    await _create(created_domains, _custom_domain(name))

    existing = await get_custom_domain(name, client=client)
    assert isinstance(existing, CustomDomain)
    existing.spec.validation_method = CustomDomainSpecValidationMethod.HTTP

    response = await update_custom_domain_detailed(name, client=client, body=existing)
    assert response.status_code == 200, response.content
    assert isinstance(response.parsed, CustomDomain)
    assert response.parsed.spec.validation_method == CustomDomainSpecValidationMethod.DNS

    fetched = await get_custom_domain(name, client=client)
    assert isinstance(fetched, CustomDomain)
    assert fetched.spec.validation_method == CustomDomainSpecValidationMethod.DNS
