from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Env")


@_attrs_define
class Env:
    """Environment variable with name and value

    Attributes:
        name (Union[Unset, str]): Name of the environment variable Example: MY_ENV_VAR.
        secret (Union[Unset, bool]): Whether the value is a secret Example: True.
        value (Union[Unset, str]): Value of the environment variable Example: my-value.
    """

    name: Union[Unset, str] = UNSET
    secret: Union[Unset, bool] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        secret = self.secret

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if secret is not UNSET:
            field_dict["secret"] = secret
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        secret = d.pop("secret", UNSET)

        value = d.pop("value", UNSET)

        env = cls(
            name=name,
            secret=secret,
            value=value,
        )

        env.additional_properties = d
        return env

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
