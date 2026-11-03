from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_connection_spec_config import IntegrationConnectionSpecConfig
    from ..models.integration_connection_spec_secret import IntegrationConnectionSpecSecret


T = TypeVar("T", bound="IntegrationConnectionSpec")


@_attrs_define
class IntegrationConnectionSpec:
    """Specification defining the integration type, configuration parameters, and encrypted credentials

    Attributes:
        config (IntegrationConnectionSpecConfig | Unset): Non-sensitive configuration parameters for the integration
            (e.g., organization ID, region)
        integration (str | Unset): Integration provider type (e.g., openai, anthropic, github, slack) Example: openai.
        sandbox (bool | Unset): Whether this connection uses sandbox/test credentials instead of production Example:
            False.
        secret (IntegrationConnectionSpecSecret | Unset): Encrypted credentials and API keys for authenticating with the
            external service
    """

    config: IntegrationConnectionSpecConfig | Unset = UNSET
    integration: str | Unset = UNSET
    sandbox: bool | Unset = UNSET
    secret: IntegrationConnectionSpecSecret | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config: dict[str, Any] | Unset = UNSET
        if self.config and not isinstance(self.config, Unset) and not isinstance(self.config, dict):
            config = self.config.to_dict()
        elif self.config and isinstance(self.config, dict):
            config = self.config

        integration = self.integration

        sandbox = self.sandbox

        secret: dict[str, Any] | Unset = UNSET
        if self.secret and not isinstance(self.secret, Unset) and not isinstance(self.secret, dict):
            secret = self.secret.to_dict()
        elif self.secret and isinstance(self.secret, dict):
            secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if integration is not UNSET:
            field_dict["integration"] = integration
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.integration_connection_spec_config import (
            IntegrationConnectionSpecConfig,  # noqa: PLC0415
        )
        from ..models.integration_connection_spec_secret import (
            IntegrationConnectionSpecSecret,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: IntegrationConnectionSpecConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = IntegrationConnectionSpecConfig.from_dict(_config)

        integration = d.pop("integration", UNSET)

        sandbox = d.pop("sandbox", UNSET)

        _secret = d.pop("secret", UNSET)
        secret: IntegrationConnectionSpecSecret | Unset
        if isinstance(_secret, Unset):
            secret = UNSET
        else:
            secret = IntegrationConnectionSpecSecret.from_dict(_secret)

        integration_connection_spec = cls(
            config=config,
            integration=integration,
            sandbox=sandbox,
            secret=secret,
        )

        integration_connection_spec.additional_properties = d
        return integration_connection_spec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
