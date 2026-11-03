from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_additional_infos import IntegrationAdditionalInfos
    from ..models.integration_endpoints import IntegrationEndpoints
    from ..models.integration_headers import IntegrationHeaders
    from ..models.integration_organization import IntegrationOrganization
    from ..models.integration_query_params import IntegrationQueryParams
    from ..models.integration_repository import IntegrationRepository


T = TypeVar("T", bound="Integration")


@_attrs_define
class Integration:
    """Integration

    Attributes:
        additional_infos (IntegrationAdditionalInfos | Unset): Integration additional infos
        endpoints (IntegrationEndpoints | Unset): Integration endpoints
        headers (IntegrationHeaders | Unset): Integration headers
        name (str | Unset): Integration name
        organizations (list[IntegrationOrganization] | Unset): Integration organizations
        params (IntegrationQueryParams | Unset): Integration query params
        repositories (list[IntegrationRepository] | Unset): Integration repositories
    """

    additional_infos: IntegrationAdditionalInfos | Unset = UNSET
    endpoints: IntegrationEndpoints | Unset = UNSET
    headers: IntegrationHeaders | Unset = UNSET
    name: str | Unset = UNSET
    organizations: list[IntegrationOrganization] | Unset = UNSET
    params: IntegrationQueryParams | Unset = UNSET
    repositories: list[IntegrationRepository] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        additional_infos: dict[str, Any] | Unset = UNSET
        if (
            self.additional_infos
            and not isinstance(self.additional_infos, Unset)
            and not isinstance(self.additional_infos, dict)
        ):
            additional_infos = self.additional_infos.to_dict()
        elif self.additional_infos and isinstance(self.additional_infos, dict):
            additional_infos = self.additional_infos

        endpoints: dict[str, Any] | Unset = UNSET
        if (
            self.endpoints
            and not isinstance(self.endpoints, Unset)
            and not isinstance(self.endpoints, dict)
        ):
            endpoints = self.endpoints.to_dict()
        elif self.endpoints and isinstance(self.endpoints, dict):
            endpoints = self.endpoints

        headers: dict[str, Any] | Unset = UNSET
        if (
            self.headers
            and not isinstance(self.headers, Unset)
            and not isinstance(self.headers, dict)
        ):
            headers = self.headers.to_dict()
        elif self.headers and isinstance(self.headers, dict):
            headers = self.headers

        name = self.name

        organizations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.organizations, Unset):
            organizations = []
            for organizations_item_data in self.organizations:
                if type(organizations_item_data) is dict:
                    organizations_item = organizations_item_data
                else:
                    organizations_item = organizations_item_data.to_dict()
                organizations.append(organizations_item)

        params: dict[str, Any] | Unset = UNSET
        if self.params and not isinstance(self.params, Unset) and not isinstance(self.params, dict):
            params = self.params.to_dict()
        elif self.params and isinstance(self.params, dict):
            params = self.params

        repositories: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = []
            for repositories_item_data in self.repositories:
                if type(repositories_item_data) is dict:
                    repositories_item = repositories_item_data
                else:
                    repositories_item = repositories_item_data.to_dict()
                repositories.append(repositories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additional_infos is not UNSET:
            field_dict["additionalInfos"] = additional_infos
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints
        if headers is not UNSET:
            field_dict["headers"] = headers
        if name is not UNSET:
            field_dict["name"] = name
        if organizations is not UNSET:
            field_dict["organizations"] = organizations
        if params is not UNSET:
            field_dict["params"] = params
        if repositories is not UNSET:
            field_dict["repositories"] = repositories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        from ..models.integration_additional_infos import (
            IntegrationAdditionalInfos,  # noqa: PLC0415
        )
        from ..models.integration_endpoints import IntegrationEndpoints  # noqa: PLC0415
        from ..models.integration_headers import IntegrationHeaders  # noqa: PLC0415
        from ..models.integration_organization import IntegrationOrganization  # noqa: PLC0415
        from ..models.integration_query_params import IntegrationQueryParams  # noqa: PLC0415
        from ..models.integration_repository import IntegrationRepository  # noqa: PLC0415

        if not src_dict:
            return None
        d = dict(src_dict)
        _additional_infos = d.pop("additionalInfos", d.pop("additional_infos", UNSET))
        additional_infos: IntegrationAdditionalInfos | Unset
        if isinstance(_additional_infos, Unset):
            additional_infos = UNSET
        else:
            additional_infos = IntegrationAdditionalInfos.from_dict(_additional_infos)

        _endpoints = d.pop("endpoints", UNSET)
        endpoints: IntegrationEndpoints | Unset
        if isinstance(_endpoints, Unset):
            endpoints = UNSET
        else:
            endpoints = IntegrationEndpoints.from_dict(_endpoints)

        _headers = d.pop("headers", UNSET)
        headers: IntegrationHeaders | Unset
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = IntegrationHeaders.from_dict(_headers)

        name = d.pop("name", UNSET)

        organizations = []
        _organizations = d.pop("organizations", UNSET)
        for organizations_item_data in _organizations or []:
            organizations_item = IntegrationOrganization.from_dict(organizations_item_data)

            organizations.append(organizations_item)

        _params = d.pop("params", UNSET)
        params: IntegrationQueryParams | Unset
        if isinstance(_params, Unset):
            params = UNSET
        else:
            params = IntegrationQueryParams.from_dict(_params)

        repositories = []
        _repositories = d.pop("repositories", UNSET)
        for repositories_item_data in _repositories or []:
            repositories_item = IntegrationRepository.from_dict(repositories_item_data)

            repositories.append(repositories_item)

        integration = cls(
            additional_infos=additional_infos,
            endpoints=endpoints,
            headers=headers,
            name=name,
            organizations=organizations,
            params=params,
            repositories=repositories,
        )

        integration.additional_properties = d
        return integration

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
