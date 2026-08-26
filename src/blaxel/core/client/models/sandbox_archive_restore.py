from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sandbox_archive_restore_state import SandboxArchiveRestoreState
from ..types import UNSET, Unset

T = TypeVar("T", bound="SandboxArchiveRestore")


@_attrs_define
class SandboxArchiveRestore:
    """Progress of the restore of a sandbox archive. A restore writes the archived filesystem over the image the sandbox
    booted from, which takes as long as the archive is big; the sandbox answers and its terminal is reachable
    throughout, but nothing may write to its filesystem until the restore is done.

        Attributes:
            files (Union[Unset, int]): Number of files restored so far (read-only)
            restored_bytes (Union[Unset, int]): Bytes of the archive restored so far (read-only)
            state (Union[Unset, SandboxArchiveRestoreState]): Phase of the restore (read-only) Example: extracting.
            total_bytes (Union[Unset, int]): Total size of the archive being restored in bytes, absent when the store did
                not announce it (read-only)
    """

    files: Union[Unset, int] = UNSET
    restored_bytes: Union[Unset, int] = UNSET
    state: Union[Unset, SandboxArchiveRestoreState] = UNSET
    total_bytes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = self.files

        restored_bytes = self.restored_bytes

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        total_bytes = self.total_bytes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if files is not UNSET:
            field_dict["files"] = files
        if restored_bytes is not UNSET:
            field_dict["restoredBytes"] = restored_bytes
        if state is not UNSET:
            field_dict["state"] = state
        if total_bytes is not UNSET:
            field_dict["totalBytes"] = total_bytes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        files = d.pop("files", UNSET)

        restored_bytes = d.pop("restoredBytes", d.pop("restored_bytes", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, SandboxArchiveRestoreState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = SandboxArchiveRestoreState(_state)

        total_bytes = d.pop("totalBytes", d.pop("total_bytes", UNSET))

        sandbox_archive_restore = cls(
            files=files,
            restored_bytes=restored_bytes,
            state=state,
            total_bytes=total_bytes,
        )

        sandbox_archive_restore.additional_properties = d
        return sandbox_archive_restore

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
