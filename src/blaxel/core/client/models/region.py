from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.region_agent_drive_public_url import RegionAgentDrivePublicUrl


T = TypeVar("T", bound="Region")


@_attrs_define
class Region:
    """Region

    Attributes:
        agent_drive_public_url (Union[Unset, RegionAgentDrivePublicUrl]): S3-compatible endpoint URL for drive storage
            in this region. Use {s3Endpoint}/{bucketName} to access drive contents.
        allowed (Union[Unset, str]): Region display name
        continent (Union[Unset, str]): Region display name
        country (Union[Unset, str]): Region display name
        drives_available (Union[Unset, bool]): Drives availability status - indicates if an S3 endpoint is configured
            for the region
        egress_available (Union[Unset, bool]): Egress availability status - indicates if network plane URL is configured
            for the region
        info_generation (Union[Unset, str]): Region display name
        location (Union[Unset, str]): Region display name
        name (Union[Unset, str]): Region name
    """

    agent_drive_public_url: Union[Unset, "RegionAgentDrivePublicUrl"] = UNSET
    allowed: Union[Unset, str] = UNSET
    continent: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    drives_available: Union[Unset, bool] = UNSET
    egress_available: Union[Unset, bool] = UNSET
    info_generation: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        agent_drive_public_url: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.agent_drive_public_url
            and not isinstance(self.agent_drive_public_url, Unset)
            and not isinstance(self.agent_drive_public_url, dict)
        ):
            agent_drive_public_url = self.agent_drive_public_url.to_dict()
        elif self.agent_drive_public_url and isinstance(self.agent_drive_public_url, dict):
            agent_drive_public_url = self.agent_drive_public_url

        allowed = self.allowed

        continent = self.continent

        country = self.country

        drives_available = self.drives_available

        egress_available = self.egress_available

        info_generation = self.info_generation

        location = self.location

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_drive_public_url is not UNSET:
            field_dict["agentDrivePublicUrl"] = agent_drive_public_url
        if allowed is not UNSET:
            field_dict["allowed"] = allowed
        if continent is not UNSET:
            field_dict["continent"] = continent
        if country is not UNSET:
            field_dict["country"] = country
        if drives_available is not UNSET:
            field_dict["drivesAvailable"] = drives_available
        if egress_available is not UNSET:
            field_dict["egressAvailable"] = egress_available
        if info_generation is not UNSET:
            field_dict["infoGeneration"] = info_generation
        if location is not UNSET:
            field_dict["location"] = location
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.region_agent_drive_public_url import RegionAgentDrivePublicUrl

        if not src_dict:
            return None
        d = src_dict.copy()
        _agent_drive_public_url = d.pop(
            "agentDrivePublicUrl", d.pop("agent_drive_public_url", UNSET)
        )
        agent_drive_public_url: Union[Unset, RegionAgentDrivePublicUrl]
        if isinstance(_agent_drive_public_url, Unset):
            agent_drive_public_url = UNSET
        else:
            agent_drive_public_url = RegionAgentDrivePublicUrl.from_dict(_agent_drive_public_url)

        allowed = d.pop("allowed", UNSET)

        continent = d.pop("continent", UNSET)

        country = d.pop("country", UNSET)

        drives_available = d.pop("drivesAvailable", d.pop("drives_available", UNSET))

        egress_available = d.pop("egressAvailable", d.pop("egress_available", UNSET))

        info_generation = d.pop("infoGeneration", d.pop("info_generation", UNSET))

        location = d.pop("location", UNSET)

        name = d.pop("name", UNSET)

        region = cls(
            agent_drive_public_url=agent_drive_public_url,
            allowed=allowed,
            continent=continent,
            country=country,
            drives_available=drives_available,
            egress_available=egress_available,
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
