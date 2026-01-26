from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FuzzySearchMatch")


@_attrs_define
class FuzzySearchMatch:
    """
    Attributes:
        path (str):  Example: src/main.go.
        score (int):  Example: 100.
        type_ (str): "file" or "directory" Example: file.
    """

    path: str
    score: int
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        score = self.score

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "score": score,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        path = d.pop("path")

        score = d.pop("score")

        type_ = d.pop("type") if "type" in d else d.pop("type_")

        fuzzy_search_match = cls(
            path=path,
            score=score,
            type_=type_,
        )

        fuzzy_search_match.additional_properties = d
        return fuzzy_search_match

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
