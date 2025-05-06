from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        additional_infos (Union[Unset, IntegrationAdditionalInfos]): Integration additional infos
        endpoints (Union[Unset, IntegrationEndpoints]): Integration endpoints
        headers (Union[Unset, IntegrationHeaders]): Integration headers
        name (Union[Unset, str]): Integration name
        organizations (Union[Unset, list['IntegrationOrganization']]): Integration organizations
        params (Union[Unset, IntegrationQueryParams]): Integration query params
        repositories (Union[Unset, list['IntegrationRepository']]): Integration repositories
    """

    additional_infos: Union[Unset, "IntegrationAdditionalInfos"] = UNSET
    endpoints: Union[Unset, "IntegrationEndpoints"] = UNSET
    headers: Union[Unset, "IntegrationHeaders"] = UNSET
    name: Union[Unset, str] = UNSET
    organizations: Union[Unset, list["IntegrationOrganization"]] = UNSET
    params: Union[Unset, "IntegrationQueryParams"] = UNSET
    repositories: Union[Unset, list["IntegrationRepository"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        additional_infos: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.additional_infos
            and not isinstance(self.additional_infos, Unset)
            and not isinstance(self.additional_infos, dict)
        ):
            additional_infos = self.additional_infos.to_dict()
        elif self.additional_infos and isinstance(self.additional_infos, dict):
            additional_infos = self.additional_infos

        endpoints: Union[Unset, dict[str, Any]] = UNSET
        if self.endpoints and not isinstance(self.endpoints, Unset) and not isinstance(self.endpoints, dict):
            endpoints = self.endpoints.to_dict()
        elif self.endpoints and isinstance(self.endpoints, dict):
            endpoints = self.endpoints

        headers: Union[Unset, dict[str, Any]] = UNSET
        if self.headers and not isinstance(self.headers, Unset) and not isinstance(self.headers, dict):
            headers = self.headers.to_dict()
        elif self.headers and isinstance(self.headers, dict):
            headers = self.headers

        name = self.name

        organizations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organizations, Unset):
            organizations = []
            for organizations_item_data in self.organizations:
                if type(organizations_item_data) == dict:
                    organizations_item = organizations_item_data
                else:
                    organizations_item = organizations_item_data.to_dict()
                organizations.append(organizations_item)

        params: Union[Unset, dict[str, Any]] = UNSET
        if self.params and not isinstance(self.params, Unset) and not isinstance(self.params, dict):
            params = self.params.to_dict()
        elif self.params and isinstance(self.params, dict):
            params = self.params

        repositories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.repositories, Unset):
            repositories = []
            for repositories_item_data in self.repositories:
                if type(repositories_item_data) == dict:
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.integration_additional_infos import IntegrationAdditionalInfos
        from ..models.integration_endpoints import IntegrationEndpoints
        from ..models.integration_headers import IntegrationHeaders
        from ..models.integration_organization import IntegrationOrganization
        from ..models.integration_query_params import IntegrationQueryParams
        from ..models.integration_repository import IntegrationRepository

        if not src_dict:
            return None
        d = src_dict.copy()
        _additional_infos = d.pop("additionalInfos", UNSET)
        additional_infos: Union[Unset, IntegrationAdditionalInfos]
        if isinstance(_additional_infos, Unset):
            additional_infos = UNSET
        else:
            additional_infos = IntegrationAdditionalInfos.from_dict(_additional_infos)

        _endpoints = d.pop("endpoints", UNSET)
        endpoints: Union[Unset, IntegrationEndpoints]
        if isinstance(_endpoints, Unset):
            endpoints = UNSET
        else:
            endpoints = IntegrationEndpoints.from_dict(_endpoints)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, IntegrationHeaders]
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
        params: Union[Unset, IntegrationQueryParams]
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
