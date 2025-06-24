from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivateCluster")


@_attrs_define
class PrivateCluster:
    """A private cluster where models can be located on.

    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        continent (Union[Unset, str]): The private cluster's continent, used to determine the closest private cluster to
            serve inference requests based on the user's location
        country (Union[Unset, str]): The country where the private cluster is located, used to determine the closest
            private cluster to serve inference requests based on the user's location
        display_name (Union[Unset, str]): The private cluster's display Name
        healthy (Union[Unset, bool]): Whether the private cluster is healthy or not, used to determine if the private
            cluster is ready to run inference
        last_health_check_time (Union[Unset, str]): The private cluster's unique name
        latitude (Union[Unset, str]): The private cluster's latitude, used to determine the closest private cluster to
            serve inference requests based on the user's location
        longitude (Union[Unset, str]): The private cluster's longitude, used to determine the closest private cluster to
            serve inference requests based on the user's location
        name (Union[Unset, str]): The name of the private cluster, it must be unique
        owned_by (Union[Unset, str]): The service account (operator) that owns the cluster
        workspace (Union[Unset, str]): The workspace the private cluster belongs to
    """

    created_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    updated_by: Union[Unset, str] = UNSET
    continent: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    healthy: Union[Unset, bool] = UNSET
    last_health_check_time: Union[Unset, str] = UNSET
    latitude: Union[Unset, str] = UNSET
    longitude: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    owned_by: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        updated_at = self.updated_at

        created_by = self.created_by

        updated_by = self.updated_by

        continent = self.continent

        country = self.country

        display_name = self.display_name

        healthy = self.healthy

        last_health_check_time = self.last_health_check_time

        latitude = self.latitude

        longitude = self.longitude

        name = self.name

        owned_by = self.owned_by

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if continent is not UNSET:
            field_dict["continent"] = continent
        if country is not UNSET:
            field_dict["country"] = country
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if healthy is not UNSET:
            field_dict["healthy"] = healthy
        if last_health_check_time is not UNSET:
            field_dict["lastHealthCheckTime"] = last_health_check_time
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if name is not UNSET:
            field_dict["name"] = name
        if owned_by is not UNSET:
            field_dict["ownedBy"] = owned_by
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        updated_by = d.pop("updatedBy", UNSET)

        continent = d.pop("continent", UNSET)

        country = d.pop("country", UNSET)

        display_name = d.pop("displayName", UNSET)

        healthy = d.pop("healthy", UNSET)

        last_health_check_time = d.pop("lastHealthCheckTime", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        name = d.pop("name", UNSET)

        owned_by = d.pop("ownedBy", UNSET)

        workspace = d.pop("workspace", UNSET)

        private_cluster = cls(
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            continent=continent,
            country=country,
            display_name=display_name,
            healthy=healthy,
            last_health_check_time=last_health_check_time,
            latitude=latitude,
            longitude=longitude,
            name=name,
            owned_by=owned_by,
            workspace=workspace,
        )

        private_cluster.additional_properties = d
        return private_cluster

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
