from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OAuth")


@_attrs_define
class OAuth:
    """OAuth of the artifact

    Attributes:
        scope (Union[Unset, list[Any]]): Scope of the OAuth
        type_ (Union[Unset, str]): Type of the OAuth
    """

    scope: Union[Unset, list[Any]] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scope is not UNSET:
            field_dict["scope"] = scope
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        scope = cast(list[Any], d.pop("scope", UNSET))

        type_ = d.pop("type", UNSET)

        o_auth = cls(
            scope=scope,
            type_=type_,
        )

        o_auth.additional_properties = d
        return o_auth

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
