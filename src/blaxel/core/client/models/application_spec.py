from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.app_revision import AppRevision
    from ..models.app_revision_configuration import AppRevisionConfiguration
    from ..models.app_url import AppUrl


T = TypeVar("T", bound="ApplicationSpec")


@_attrs_define
class ApplicationSpec:
    """Configuration for an application including revision management, URL routing, and deployment region

    Attributes:
        enabled (Union[Unset, bool]): When false, the application is disabled and will not serve requests Default: True.
            Example: True.
        port (Union[Unset, int]): Port the application listens on (default 8080) Example: 8080.
        region (Union[Unset, str]): Region where the application is deployed (e.g. us-pdx-1, eu-lon-1) Example: us-
            pdx-1.
        revision (Union[Unset, AppRevisionConfiguration]): Routing configuration controlling which revision is active
            and canary traffic splitting
        revisions (Union[Unset, list['AppRevision']]):
        urls (Union[Unset, list['AppUrl']]): URL configuration for the application. Each entry defines a custom URL
            through which the application is accessible. The domain must be a verified custom domain in the workspace.
    """

    enabled: Union[Unset, bool] = True
    port: Union[Unset, int] = UNSET
    region: Union[Unset, str] = UNSET
    revision: Union[Unset, "AppRevisionConfiguration"] = UNSET
    revisions: Union[Unset, list["AppRevision"]] = UNSET
    urls: Union[Unset, list["AppUrl"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        enabled = self.enabled

        port = self.port

        region = self.region

        revision: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.revision
            and not isinstance(self.revision, Unset)
            and not isinstance(self.revision, dict)
        ):
            revision = self.revision.to_dict()
        elif self.revision and isinstance(self.revision, dict):
            revision = self.revision

        revisions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.revisions, Unset):
            revisions = []
            for componentsschemas_app_revisions_item_data in self.revisions:
                if type(componentsschemas_app_revisions_item_data) is dict:
                    componentsschemas_app_revisions_item = componentsschemas_app_revisions_item_data
                else:
                    componentsschemas_app_revisions_item = (
                        componentsschemas_app_revisions_item_data.to_dict()
                    )
                revisions.append(componentsschemas_app_revisions_item)

        urls: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.urls, Unset):
            urls = []
            for componentsschemas_app_urls_item_data in self.urls:
                if type(componentsschemas_app_urls_item_data) is dict:
                    componentsschemas_app_urls_item = componentsschemas_app_urls_item_data
                else:
                    componentsschemas_app_urls_item = componentsschemas_app_urls_item_data.to_dict()
                urls.append(componentsschemas_app_urls_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if port is not UNSET:
            field_dict["port"] = port
        if region is not UNSET:
            field_dict["region"] = region
        if revision is not UNSET:
            field_dict["revision"] = revision
        if revisions is not UNSET:
            field_dict["revisions"] = revisions
        if urls is not UNSET:
            field_dict["urls"] = urls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.app_revision import AppRevision
        from ..models.app_revision_configuration import AppRevisionConfiguration
        from ..models.app_url import AppUrl

        if not src_dict:
            return None
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        port = d.pop("port", UNSET)

        region = d.pop("region", UNSET)

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, AppRevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = AppRevisionConfiguration.from_dict(_revision)

        revisions = []
        _revisions = d.pop("revisions", UNSET)
        for componentsschemas_app_revisions_item_data in _revisions or []:
            componentsschemas_app_revisions_item = AppRevision.from_dict(
                componentsschemas_app_revisions_item_data
            )

            revisions.append(componentsschemas_app_revisions_item)

        urls = []
        _urls = d.pop("urls", UNSET)
        for componentsschemas_app_urls_item_data in _urls or []:
            componentsschemas_app_urls_item = AppUrl.from_dict(componentsschemas_app_urls_item_data)

            urls.append(componentsschemas_app_urls_item)

        application_spec = cls(
            enabled=enabled,
            port=port,
            region=region,
            revision=revision,
            revisions=revisions,
            urls=urls,
        )

        application_spec.additional_properties = d
        return application_spec

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
