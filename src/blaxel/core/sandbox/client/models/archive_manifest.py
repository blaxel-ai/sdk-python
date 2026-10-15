from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArchiveManifest")


@_attrs_define
class ArchiveManifest:
    """
    Attributes:
        created_at (str):
        root (str): Root is the directory the paths are relative to. Example: /.
        version (int):  Example: 1.
        added (Union[Unset, int]): Added and Modified count the archive's payload members. Example: 11.
        api_version (Union[Unset, str]): APIVersion is the sandbox-api build that produced the archive. Example: v0.1.0.
        deleted (Union[Unset, list[str]]): Deleted are paths the image has and the sandbox deleted. Tar cannot carry
            a deletion, so import applies these from the manifest.
        excludes (Union[Unset, list[str]]): Excludes are the paths left out of the comparison.
        image_device (Union[Unset, str]): ImageDevice is the device the pristine image was read from, for the record:
            it says where the sandbox that exported the archive found its image. Example: /dev/vda.
        modified (Union[Unset, int]):  Example: 3.
        payload_bytes (Union[Unset, int]): PayloadBytes is the total content size of the payload members. Example:
            3073449.
        processes (Union[Unset, bool]): Processes tells whether ProcessesName is present. Example: True.
    """

    created_at: str
    root: str
    version: int
    added: Union[Unset, int] = UNSET
    api_version: Union[Unset, str] = UNSET
    deleted: Union[Unset, list[str]] = UNSET
    excludes: Union[Unset, list[str]] = UNSET
    image_device: Union[Unset, str] = UNSET
    modified: Union[Unset, int] = UNSET
    payload_bytes: Union[Unset, int] = UNSET
    processes: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        root = self.root

        version = self.version

        added = self.added

        api_version = self.api_version

        deleted: Union[Unset, list[str]] = UNSET
        if not isinstance(self.deleted, Unset):
            deleted = self.deleted

        excludes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.excludes, Unset):
            excludes = self.excludes

        image_device = self.image_device

        modified = self.modified

        payload_bytes = self.payload_bytes

        processes = self.processes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "root": root,
                "version": version,
            }
        )
        if added is not UNSET:
            field_dict["added"] = added
        if api_version is not UNSET:
            field_dict["apiVersion"] = api_version
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if excludes is not UNSET:
            field_dict["excludes"] = excludes
        if image_device is not UNSET:
            field_dict["imageDevice"] = image_device
        if modified is not UNSET:
            field_dict["modified"] = modified
        if payload_bytes is not UNSET:
            field_dict["payloadBytes"] = payload_bytes
        if processes is not UNSET:
            field_dict["processes"] = processes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        created_at = d.pop("createdAt") if "createdAt" in d else d.pop("created_at")

        root = d.pop("root")

        version = d.pop("version")

        added = d.pop("added", UNSET)

        api_version = d.pop("apiVersion", d.pop("api_version", UNSET))

        deleted = cast(list[str], d.pop("deleted", UNSET))

        excludes = cast(list[str], d.pop("excludes", UNSET))

        image_device = d.pop("imageDevice", d.pop("image_device", UNSET))

        modified = d.pop("modified", UNSET)

        payload_bytes = d.pop("payloadBytes", d.pop("payload_bytes", UNSET))

        processes = d.pop("processes", UNSET)

        archive_manifest = cls(
            created_at=created_at,
            root=root,
            version=version,
            added=added,
            api_version=api_version,
            deleted=deleted,
            excludes=excludes,
            image_device=image_device,
            modified=modified,
            payload_bytes=payload_bytes,
            processes=processes,
        )

        archive_manifest.additional_properties = d
        return archive_manifest

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
