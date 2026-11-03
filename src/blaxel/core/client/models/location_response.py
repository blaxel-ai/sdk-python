from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flavor import Flavor


T = TypeVar("T", bound="LocationResponse")


@_attrs_define
class LocationResponse:
    """Location availability for policies

    Attributes:
        continent (str | Unset): Continent of the location Example: NA.
        country (str | Unset): Country of the location Example: US.
        flavors (list[Flavor] | Unset): Hardware flavors available in the location
        location (str | Unset): Name of the location Example: Portland.
        region (str | Unset): Region of the location Example: us-pdx-1.
        status (str | Unset): Status of the location Example: healthy.
    """

    continent: str | Unset = UNSET
    country: str | Unset = UNSET
    flavors: list[Flavor] | Unset = UNSET
    location: str | Unset = UNSET
    region: str | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        continent = self.continent

        country = self.country

        flavors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for flavors_item_data in self.flavors:
                if type(flavors_item_data) is dict:
                    flavors_item = flavors_item_data
                else:
                    flavors_item = flavors_item_data.to_dict()
                flavors.append(flavors_item)

        location = self.location

        region = self.region

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if continent is not UNSET:
            field_dict["continent"] = continent
        if country is not UNSET:
            field_dict["country"] = country
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if location is not UNSET:
            field_dict["location"] = location
        if region is not UNSET:
            field_dict["region"] = region
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.flavor import Flavor  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        continent = d.pop("continent", UNSET)

        country = d.pop("country", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for flavors_item_data in _flavors or []:
            flavors_item = Flavor.from_dict(flavors_item_data)

            flavors.append(flavors_item)

        location = d.pop("location", UNSET)

        region = d.pop("region", UNSET)

        status = d.pop("status", UNSET)

        location_response = cls(
            continent=continent,
            country=country,
            flavors=flavors,
            location=location,
            region=region,
            status=status,
        )

        location_response.additional_properties = d
        return location_response

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
