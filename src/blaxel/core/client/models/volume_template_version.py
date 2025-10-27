from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VolumeTemplateVersion")


@_attrs_define
class VolumeTemplateVersion:
    """Volume template version tracking individual versions of template content

    Attributes:
        bucket (Union[Unset, str]): S3 bucket name where this version is stored
        content_size (Union[Unset, int]): Size of the template content in bytes
        name (Union[Unset, str]): Name of the template version
        region (Union[Unset, str]): AWS region where this version is stored
        status (Union[Unset, str]): Status of the version (CREATED, READY, FAILED)
        template_name (Union[Unset, str]): Template name this version belongs to
        version_id (Union[Unset, str]): S3 version ID for this template version
        workspace (Union[Unset, str]): Workspace name
    """

    bucket: Union[Unset, str] = UNSET
    content_size: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    template_name: Union[Unset, str] = UNSET
    version_id: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket = self.bucket

        content_size = self.content_size

        name = self.name

        region = self.region

        status = self.status

        template_name = self.template_name

        version_id = self.version_id

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bucket is not UNSET:
            field_dict["bucket"] = bucket
        if content_size is not UNSET:
            field_dict["contentSize"] = content_size
        if name is not UNSET:
            field_dict["name"] = name
        if region is not UNSET:
            field_dict["region"] = region
        if status is not UNSET:
            field_dict["status"] = status
        if template_name is not UNSET:
            field_dict["templateName"] = template_name
        if version_id is not UNSET:
            field_dict["versionId"] = version_id
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        bucket = d.pop("bucket", UNSET)

        content_size = d.pop("contentSize", UNSET)

        name = d.pop("name", UNSET)

        region = d.pop("region", UNSET)

        status = d.pop("status", UNSET)

        template_name = d.pop("templateName", UNSET)

        version_id = d.pop("versionId", UNSET)

        workspace = d.pop("workspace", UNSET)

        volume_template_version = cls(
            bucket=bucket,
            content_size=content_size,
            name=name,
            region=region,
            status=status,
            template_name=template_name,
            version_id=version_id,
            workspace=workspace,
        )

        volume_template_version.additional_properties = d
        return volume_template_version

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
