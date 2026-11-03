from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.archive_export_state import ArchiveExportState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportProgress")


@_attrs_define
class ExportProgress:
    """
    Attributes:
        error (str | Unset): Error is why the export failed, without the presigned URL it used.
        finished_at (str | Unset):
        size (int | Unset): Size is the archive's exact size, known once the filesystem is scanned. Example: 3074211.
        started_at (str | Unset):
        state (ArchiveExportState | Unset):
        uploaded (bool | Unset): Uploaded reports whether the storage holds the archive. Example: False.
    """

    error: str | Unset = UNSET
    finished_at: str | Unset = UNSET
    size: int | Unset = UNSET
    started_at: str | Unset = UNSET
    state: ArchiveExportState | Unset = UNSET
    uploaded: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        finished_at = self.finished_at

        size = self.size

        started_at = self.started_at

        state: str | Unset = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        uploaded = self.uploaded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if size is not UNSET:
            field_dict["size"] = size
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if state is not UNSET:
            field_dict["state"] = state
        if uploaded is not UNSET:
            field_dict["uploaded"] = uploaded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = dict(src_dict)
        error = d.pop("error", UNSET)

        finished_at = d.pop("finishedAt", d.pop("finished_at", UNSET))

        size = d.pop("size", UNSET)

        started_at = d.pop("startedAt", d.pop("started_at", UNSET))

        _state = d.pop("state", UNSET)
        state: ArchiveExportState | Unset
        if isinstance(_state, Unset) or _state == "":
            state = UNSET
        else:
            state = ArchiveExportState(_state)

        uploaded = d.pop("uploaded", UNSET)

        export_progress = cls(
            error=error,
            finished_at=finished_at,
            size=size,
            started_at=started_at,
            state=state,
            uploaded=uploaded,
        )

        export_progress.additional_properties = d
        return export_progress

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
