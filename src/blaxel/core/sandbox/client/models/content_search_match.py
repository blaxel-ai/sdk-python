from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContentSearchMatch")


@_attrs_define
class ContentSearchMatch:
    """
    Attributes:
        column (int):  Example: 10.
        line (int):  Example: 42.
        path (str):  Example: src/main.go.
        text (str):  Example: const searchText = 'example'.
        context (Union[Unset, str]):  Example: previous line
            current line
            next line.
    """

    column: int
    line: int
    path: str
    text: str
    context: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        column = self.column

        line = self.line

        path = self.path

        text = self.text

        context = self.context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "column": column,
                "line": line,
                "path": path,
                "text": text,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        column = d.pop("column")

        line = d.pop("line")

        path = d.pop("path")

        text = d.pop("text")

        context = d.pop("context", UNSET)

        content_search_match = cls(
            column=column,
            line=line,
            path=path,
            text=text,
            context=context,
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
