from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FuzzySearchMatch")


@_attrs_define
class FuzzySearchMatch:
    """
    Attributes:
        path (Union[Unset, str]):  Example: src/main.go.
        score (Union[Unset, int]):  Example: 100.
        type_ (Union[Unset, str]): "file" or "directory" Example: file.
    """

    path: Union[Unset, str] = UNSET
    score: Union[Unset, int] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        score = self.score

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if score is not UNSET:
            field_dict["score"] = score
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        score = d.pop("score", UNSET)

        type_ = d.pop("type", d.pop("type_", UNSET))

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
