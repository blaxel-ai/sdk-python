from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewSpec")


@_attrs_define
class PreviewSpec:
    """Preview of a Resource

    Attributes:
        port (Union[Unset, int]): Port of the preview
        public (Union[Unset, bool]): Whether the preview is public
        url (Union[Unset, str]): URL of the preview
    """

    port: Union[Unset, int] = UNSET
    public: Union[Unset, bool] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        port = self.port

        public = self.public

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if port is not UNSET:
            field_dict["port"] = port
        if public is not UNSET:
            field_dict["public"] = public
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        port = d.pop("port", UNSET)

        public = d.pop("public", UNSET)

        url = d.pop("url", UNSET)

        preview_spec = cls(
            port=port,
            public=public,
            url=url,
        )

        preview_spec.additional_properties = d
        return preview_spec

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
