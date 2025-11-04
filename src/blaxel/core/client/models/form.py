from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.form_config import FormConfig
    from ..models.form_oauth import FormOauth
    from ..models.form_secrets import FormSecrets


T = TypeVar("T", bound="Form")


@_attrs_define
class Form:
    """Form of the artifact

    Attributes:
        config (Union[Unset, FormConfig]): Config of the artifact
        oauth (Union[Unset, FormOauth]): OAuth of the artifact
        secrets (Union[Unset, FormSecrets]): Secrets of the artifact
    """

    config: Union[Unset, "FormConfig"] = UNSET
    oauth: Union[Unset, "FormOauth"] = UNSET
    secrets: Union[Unset, "FormSecrets"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config: Union[Unset, dict[str, Any]] = UNSET
        if self.config and not isinstance(self.config, Unset) and not isinstance(self.config, dict):
            config = self.config.to_dict()
        elif self.config and isinstance(self.config, dict):
            config = self.config

        oauth: Union[Unset, dict[str, Any]] = UNSET
        if self.oauth and not isinstance(self.oauth, Unset) and not isinstance(self.oauth, dict):
            oauth = self.oauth.to_dict()
        elif self.oauth and isinstance(self.oauth, dict):
            oauth = self.oauth

        secrets: Union[Unset, dict[str, Any]] = UNSET
        if self.secrets and not isinstance(self.secrets, Unset) and not isinstance(self.secrets, dict):
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.form_config import FormConfig
        from ..models.form_oauth import FormOauth
        from ..models.form_secrets import FormSecrets

        if not src_dict:
            return None
        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, FormConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = FormConfig.from_dict(_config)

        _oauth = d.pop("oauth", UNSET)
        oauth: Union[Unset, FormOauth]
        if isinstance(_oauth, Unset):
            oauth = UNSET
        else:
            oauth = FormOauth.from_dict(_oauth)

        _secrets = d.pop("secrets", UNSET)
        secrets: Union[Unset, FormSecrets]
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
