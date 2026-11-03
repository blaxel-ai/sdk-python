from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.form_config import FormConfig
    from ..models.form_secrets import FormSecrets
    from ..models.o_auth import OAuth


T = TypeVar("T", bound="Form")


@_attrs_define
class Form:
    """Form of the artifact

    Attributes:
        config (FormConfig | Unset): Config of the artifact
        oauth (OAuth | Unset): OAuth of the artifact
        secrets (FormSecrets | Unset): Secrets of the artifact
    """

    config: FormConfig | Unset = UNSET
    oauth: OAuth | Unset = UNSET
    secrets: FormSecrets | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config: dict[str, Any] | Unset = UNSET
        if self.config and not isinstance(self.config, Unset) and not isinstance(self.config, dict):
            config = self.config.to_dict()
        elif self.config and isinstance(self.config, dict):
            config = self.config

        oauth: dict[str, Any] | Unset = UNSET
        if self.oauth and not isinstance(self.oauth, Unset) and not isinstance(self.oauth, dict):
            oauth = self.oauth.to_dict()
        elif self.oauth and isinstance(self.oauth, dict):
            oauth = self.oauth

        secrets: dict[str, Any] | Unset = UNSET
        if (
            self.secrets
            and not isinstance(self.secrets, Unset)
            and not isinstance(self.secrets, dict)
        ):
            secrets = self.secrets.to_dict()
        elif self.secrets and isinstance(self.secrets, dict):
            secrets = self.secrets

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if oauth is not UNSET:
            field_dict["oauth"] = oauth
        if secrets is not UNSET:
            field_dict["secrets"] = secrets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.form_config import FormConfig  # noqa: PLC0415
        from ..models.form_secrets import FormSecrets  # noqa: PLC0415
        from ..models.o_auth import OAuth  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: FormConfig | Unset
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FormConfig.from_dict(_config)

        _oauth = d.pop("oauth", UNSET)
        oauth: OAuth | Unset
        if isinstance(_oauth, Unset):
            oauth = UNSET
        else:
            oauth = OAuth.from_dict(_oauth)

        _secrets = d.pop("secrets", UNSET)
        secrets: FormSecrets | Unset
        if isinstance(_secrets, Unset):
            secrets = UNSET
        else:
            secrets = FormSecrets.from_dict(_secrets)

        form = cls(
            config=config,
            oauth=oauth,
            secrets=secrets,
        )

        form.additional_properties = d
        return form

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
