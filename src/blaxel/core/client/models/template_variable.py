from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TemplateVariable")


@_attrs_define
class TemplateVariable:
    """Blaxel template variable

    Attributes:
        description (Union[Unset, str]): Description of the variable
        integration (Union[Unset, str]): Integration of the variable
        name (Union[Unset, str]): Name of the variable
        path (Union[Unset, str]): Path of the variable
        secret (Union[Unset, bool]): Whether the variable is secret
    """

    description: Union[Unset, str] = UNSET
    integration: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    secret: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        integration = self.integration

        name = self.name

        path = self.path

        secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if integration is not UNSET:
            field_dict["integration"] = integration
        if name is not UNSET:
            field_dict["name"] = name
        if path is not UNSET:
            field_dict["path"] = path
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        integration = d.pop("integration", UNSET)

        name = d.pop("name", UNSET)

        path = d.pop("path", UNSET)

        secret = d.pop("secret", UNSET)

        template_variable = cls(
            description=description,
            integration=integration,
            name=name,
            path=path,
            secret=secret,
        )

        template_variable.additional_properties = d
        return template_variable

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
