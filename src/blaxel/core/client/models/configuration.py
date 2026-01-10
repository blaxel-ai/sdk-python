from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.continent import Continent
    from ..models.country import Country
    from ..models.private_location import PrivateLocation
    from ..models.region import Region


T = TypeVar("T", bound="Configuration")


@_attrs_define
class Configuration:
    """Configuration

    Attributes:
        continents (Union[Unset, list['Continent']]): Continents
        countries (Union[Unset, list['Country']]): Countries
        private_locations (Union[Unset, list['PrivateLocation']]): Private locations managed with blaxel operator
        regions (Union[Unset, list['Region']]): Regions
    """

    continents: Union[Unset, list["Continent"]] = UNSET
    countries: Union[Unset, list["Country"]] = UNSET
    private_locations: Union[Unset, list["PrivateLocation"]] = UNSET
    regions: Union[Unset, list["Region"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        continents: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.continents, Unset):
            continents = []
            for continents_item_data in self.continents:
                if type(continents_item_data) is dict:
                    continents_item = continents_item_data
                else:
                    continents_item = continents_item_data.to_dict()
                continents.append(continents_item)

        countries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.countries, Unset):
            countries = []
            for countries_item_data in self.countries:
                if type(countries_item_data) is dict:
                    countries_item = countries_item_data
                else:
                    countries_item = countries_item_data.to_dict()
                countries.append(countries_item)

        private_locations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.private_locations, Unset):
            private_locations = []
            for private_locations_item_data in self.private_locations:
                if type(private_locations_item_data) is dict:
                    private_locations_item = private_locations_item_data
                else:
                    private_locations_item = private_locations_item_data.to_dict()
                private_locations.append(private_locations_item)

        regions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.regions, Unset):
            regions = []
            for regions_item_data in self.regions:
                if type(regions_item_data) is dict:
                    regions_item = regions_item_data
                else:
                    regions_item = regions_item_data.to_dict()
                regions.append(regions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if continents is not UNSET:
            field_dict["continents"] = continents
        if countries is not UNSET:
            field_dict["countries"] = countries
        if private_locations is not UNSET:
            field_dict["privateLocations"] = private_locations
        if regions is not UNSET:
            field_dict["regions"] = regions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.continent import Continent
        from ..models.country import Country
        from ..models.private_location import PrivateLocation
        from ..models.region import Region

        if not src_dict:
            return None
        d = src_dict.copy()
        continents = []
        _continents = d.pop("continents", UNSET)
        for continents_item_data in _continents or []:
            continents_item = Continent.from_dict(continents_item_data)

            continents.append(continents_item)

        countries = []
        _countries = d.pop("countries", UNSET)
        for countries_item_data in _countries or []:
            countries_item = Country.from_dict(countries_item_data)

            countries.append(countries_item)

        private_locations = []
        _private_locations = d.pop("privateLocations", d.pop("private_locations", UNSET))
        for private_locations_item_data in _private_locations or []:
            private_locations_item = PrivateLocation.from_dict(private_locations_item_data)

            private_locations.append(private_locations_item)

        regions = []
        _regions = d.pop("regions", UNSET)
        for regions_item_data in _regions or []:
            regions_item = Region.from_dict(regions_item_data)

            regions.append(regions_item)

        configuration = cls(
            continents=continents,
            countries=countries,
            private_locations=private_locations,
            regions=regions,
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
