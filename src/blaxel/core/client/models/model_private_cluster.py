from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelPrivateCluster")


@_attrs_define
class ModelPrivateCluster:
    """Private cluster where the model deployment is deployed

    Attributes:
        base_url (Union[Unset, str]): The base url of the model in the private cluster
        enabled (Union[Unset, bool]): If true, the private cluster is available
        name (Union[Unset, str]): The name of the private cluster
    """

    base_url: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_url = self.base_url

        enabled = self.enabled

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        base_url = d.pop("baseUrl", UNSET)

        enabled = d.pop("enabled", UNSET)

        name = d.pop("name", UNSET)

        model_private_cluster = cls(
            base_url=base_url,
            enabled=enabled,
            name=name,
        )

        model_private_cluster.additional_properties = d
        return model_private_cluster

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
