from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Configuration")


@_attrs_define
class Configuration:
    """Configuration

    Attributes:
        continents (Union[Unset, list[Any]]): Continents
        countries (Union[Unset, list[Any]]): Countries
        private_locations (Union[Unset, list[Any]]): Private locations managed with blaxel operator
    """

    continents: Union[Unset, list[Any]] = UNSET
    countries: Union[Unset, list[Any]] = UNSET
    private_locations: Union[Unset, list[Any]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        continents: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.continents, Unset):
            continents = self.continents

        countries: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.countries, Unset):
            countries = self.countries

        private_locations: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.private_locations, Unset):
            private_locations = self.private_locations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if continents is not UNSET:
            field_dict["continents"] = continents
        if countries is not UNSET:
            field_dict["countries"] = countries
        if private_locations is not UNSET:
            field_dict["privateLocations"] = private_locations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        continents = cast(list[Any], d.pop("continents", UNSET))

        countries = cast(list[Any], d.pop("countries", UNSET))

        private_locations = cast(list[Any], d.pop("privateLocations", UNSET))

        configuration = cls(
            continents=continents,
            countries=countries,
            private_locations=private_locations,
        )

        configuration.additional_properties = d
        return configuration

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
