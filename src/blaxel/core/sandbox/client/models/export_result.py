from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.archive_change import ArchiveChange
    from ..models.archive_manifest import ArchiveManifest


T = TypeVar("T", bound="ExportResult")


@_attrs_define
class ExportResult:
    """
    Attributes:
        manifest (ArchiveManifest):
        changes (Union[Unset, list['ArchiveChange']]): Changes lists every path in the archive. Only filled for a dry
            run,
            where it is the point of the call.
        duration (Union[Unset, str]):  Example: 4.2s.
        size (Union[Unset, int]): Size is the exact number of bytes uploaded, known before the upload
            starts since the archive is not compressed. Example: 3074211.
        stopped_processes (Union[Unset, list[str]]): StoppedProcesses are the processes stopped to freeze the
            filesystem.
        uploaded (Union[Unset, bool]): Uploaded is false for a dry run. Example: True.
    """

    manifest: "ArchiveManifest"
    changes: Union[Unset, list["ArchiveChange"]] = UNSET
    duration: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    stopped_processes: Union[Unset, list[str]] = UNSET
    uploaded: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        if type(self.manifest) is dict:
            manifest = self.manifest
        else:
            manifest = self.manifest.to_dict()

        changes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.changes, Unset):
            changes = []
            for changes_item_data in self.changes:
                if type(changes_item_data) is dict:
                    changes_item = changes_item_data
                else:
                    changes_item = changes_item_data.to_dict()
                changes.append(changes_item)

        duration = self.duration

        size = self.size

        stopped_processes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.stopped_processes, Unset):
            stopped_processes = self.stopped_processes

        uploaded = self.uploaded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "manifest": manifest,
            }
        )
        if changes is not UNSET:
            field_dict["changes"] = changes
        if duration is not UNSET:
            field_dict["duration"] = duration
        if size is not UNSET:
            field_dict["size"] = size
        if stopped_processes is not UNSET:
            field_dict["stoppedProcesses"] = stopped_processes
        if uploaded is not UNSET:
            field_dict["uploaded"] = uploaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.archive_change import ArchiveChange
        from ..models.archive_manifest import ArchiveManifest

        if not src_dict:
            return None
        d = src_dict.copy()
        manifest = ArchiveManifest.from_dict(d.pop("manifest"))

        changes = []
        _changes = d.pop("changes", UNSET)
        for changes_item_data in _changes or []:
            changes_item = ArchiveChange.from_dict(changes_item_data)

            changes.append(changes_item)

        duration = d.pop("duration", UNSET)

        size = d.pop("size", UNSET)

        stopped_processes = cast(
            list[str], d.pop("stoppedProcesses", d.pop("stopped_processes", UNSET))
        )

        uploaded = d.pop("uploaded", UNSET)

        export_result = cls(
            manifest=manifest,
            changes=changes,
            duration=duration,
            size=size,
            stopped_processes=stopped_processes,
            uploaded=uploaded,
        )

        export_result.additional_properties = d
        return export_result

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
