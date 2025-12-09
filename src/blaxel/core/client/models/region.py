from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Region")


@_attrs_define
class Region:
    """Region

    Attributes:
        allowed (Union[Unset, str]): Region display name
        continent (Union[Unset, str]): Region display name
        country (Union[Unset, str]): Region display name
        info_generation (Union[Unset, str]): Region display name
        location (Union[Unset, str]): Region display name
        name (Union[Unset, str]): Region name
    """

    allowed: Union[Unset, str] = UNSET
    continent: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    info_generation: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed = self.allowed

        continent = self.continent

        country = self.country

        info_generation = self.info_generation

        location = self.location

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed is not UNSET:
            field_dict["allowed"] = allowed
        if continent is not UNSET:
            field_dict["continent"] = continent
        if country is not UNSET:
            field_dict["country"] = country
        if info_generation is not UNSET:
            field_dict["infoGeneration"] = info_generation
        if location is not UNSET:
            field_dict["location"] = location
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        allowed = d.pop("allowed", UNSET)

        continent = d.pop("continent", UNSET)

        country = d.pop("country", UNSET)

        info_generation = d.pop("infoGeneration", d.pop("info_generation", UNSET))

        location = d.pop("location", UNSET)

        name = d.pop("name", UNSET)

        region = cls(
            allowed=allowed,
            continent=continent,
            country=country,
            info_generation=info_generation,
            location=location,
            name=name,
        )

        region.additional_properties = d
        return region

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
