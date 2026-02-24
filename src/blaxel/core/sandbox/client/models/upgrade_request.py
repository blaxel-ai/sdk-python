from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpgradeRequest")


@_attrs_define
class UpgradeRequest:
    """
    Attributes:
        base_url (Union[Unset, str]): Base URL for releases (useful for forks) Example: https://github.com/blaxel-
            ai/sandbox/releases.
        version (Union[Unset, str]): Version to upgrade to: "develop", "main", "latest", or specific tag like "v1.0.0"
            Example: develop.
    """

    base_url: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_url = self.base_url

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        base_url = d.pop("baseUrl", d.pop("base_url", UNSET))

        version = d.pop("version", UNSET)

        upgrade_request = cls(
            base_url=base_url,
            version=version,
        )

        upgrade_request.additional_properties = d
        return upgrade_request

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
