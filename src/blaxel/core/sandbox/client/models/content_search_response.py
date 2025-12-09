from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_search_match import ContentSearchMatch


T = TypeVar("T", bound="ContentSearchResponse")


@_attrs_define
class ContentSearchResponse:
    """
    Attributes:
        matches (Union[Unset, list['ContentSearchMatch']]):
        query (Union[Unset, str]):  Example: searchText.
        total (Union[Unset, int]):  Example: 5.
    """

    matches: Union[Unset, list["ContentSearchMatch"]] = UNSET
    query: Union[Unset, str] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        matches: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.matches, Unset):
            matches = []
            for matches_item_data in self.matches:
                if type(matches_item_data) is dict:
                    matches_item = matches_item_data
                else:
                    matches_item = matches_item_data.to_dict()
                matches.append(matches_item)

        query = self.query

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if matches is not UNSET:
            field_dict["matches"] = matches
        if query is not UNSET:
            field_dict["query"] = query
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.content_search_match import ContentSearchMatch

        if not src_dict:
            return None
        d = src_dict.copy()
        matches = []
        _matches = d.pop("matches", UNSET)
        for matches_item_data in _matches or []:
            matches_item = ContentSearchMatch.from_dict(matches_item_data)

            matches.append(matches_item)

        query = d.pop("query", UNSET)

        total = d.pop("total", UNSET)

        content_search_response = cls(
            matches=matches,
            query=query,
            total=total,
        )

        content_search_response.additional_properties = d
        return content_search_response

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
