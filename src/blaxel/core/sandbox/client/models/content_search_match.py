from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContentSearchMatch")


@_attrs_define
class ContentSearchMatch:
    """
    Attributes:
        column (Union[Unset, int]):  Example: 10.
        context (Union[Unset, str]):  Example: previous line
            current line
            next line.
        line (Union[Unset, int]):  Example: 42.
        path (Union[Unset, str]):  Example: src/main.go.
        text (Union[Unset, str]):  Example: const searchText = 'example'.
    """

    column: Union[Unset, int] = UNSET
    context: Union[Unset, str] = UNSET
    line: Union[Unset, int] = UNSET
    path: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        context = self.context

        line = self.line

        path = self.path

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if column is not UNSET:
            field_dict["column"] = column
        if context is not UNSET:
            field_dict["context"] = context
        if line is not UNSET:
            field_dict["line"] = line
        if path is not UNSET:
            field_dict["path"] = path
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        column = d.pop("column", UNSET)

        context = d.pop("context", UNSET)

        line = d.pop("line", UNSET)

        path = d.pop("path", UNSET)

        text = d.pop("text", UNSET)

        content_search_match = cls(
            column=column,
            context=context,
            line=line,
            path=path,
            text=text,
        )

        content_search_match.additional_properties = d
        return content_search_match

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
