from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

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
        agent_drive_public_url (RegionAgentDrivePublicUrl | Unset): S3-compatible endpoint URL for drive storage in this
            region. Use {s3Endpoint}/{bucketName} to access drive contents.
        allowed (str | Unset): Region display name
        continent (str | Unset): Region display name
        country (str | Unset): Region display name
        drives_available (bool | Unset): Drives availability status - indicates if an S3 endpoint is configured for the
            region
        egress_available (bool | Unset): Egress availability status - indicates if network plane URL is configured for
            the region
        info_generation (str | Unset): Region display name
        location (str | Unset): Region display name
        mk_31_available (bool | Unset): Whether this region supports mk3.1 (blaxel nodes). Required for Application and
            Job deployments.
        name (str | Unset): Region name
        proxy_available (bool | Unset): Proxy availability status - indicates if the proxy plane is configured for the
            region
    """

    agent_drive_public_url: RegionAgentDrivePublicUrl | Unset = UNSET
    allowed: str | Unset = UNSET
    continent: str | Unset = UNSET
    country: str | Unset = UNSET
    drives_available: bool | Unset = UNSET
    egress_available: bool | Unset = UNSET
    info_generation: str | Unset = UNSET
    location: str | Unset = UNSET
    mk_31_available: bool | Unset = UNSET
    name: str | Unset = UNSET
    proxy_available: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_drive_public_url: dict[str, Any] | Unset = UNSET
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

        mk_31_available = self.mk_31_available

        name = self.name

        proxy_available = self.proxy_available

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
        if mk_31_available is not UNSET:
            field_dict["mk31Available"] = mk_31_available
        if name is not UNSET:
            field_dict["name"] = name
        if proxy_available is not UNSET:
            field_dict["proxyAvailable"] = proxy_available

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.region_agent_drive_public_url import (
            RegionAgentDrivePublicUrl,  # noqa: PLC0415
        )

        if not src_dict:
            return None
        d = dict(src_dict)
        _agent_drive_public_url = d.pop(
            "agentDrivePublicUrl", d.pop("agent_drive_public_url", UNSET)
        )
        agent_drive_public_url: RegionAgentDrivePublicUrl | Unset
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

        mk_31_available = d.pop("mk31Available", d.pop("mk_31_available", UNSET))

        name = d.pop("name", UNSET)

        proxy_available = d.pop("proxyAvailable", d.pop("proxy_available", UNSET))

        region = cls(
            agent_drive_public_url=agent_drive_public_url,
            allowed=allowed,
            continent=continent,
            country=country,
            drives_available=drives_available,
            egress_available=egress_available,
            info_generation=info_generation,
            location=location,
            mk_31_available=mk_31_available,
            name=name,
            proxy_available=proxy_available,
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
