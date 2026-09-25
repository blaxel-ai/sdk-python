from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.archive_restore_state import ArchiveRestoreState
from ..types import UNSET, Unset

T = TypeVar("T", bound="RestoreProgress")


@_attrs_define
class RestoreProgress:
    """
    Attributes:
        deleted (Union[Unset, int]):  Example: 3.
        downloaded (Union[Unset, int]): Downloaded is how much of the archive has been read so far. Example: 1048576.
        error (Union[Unset, str]): Error is why the restore failed, without the presigned URL it used.
        finished_at (Union[Unset, str]):
        restored (Union[Unset, int]): Restored and Deleted count what the archive changed on the filesystem. Example:
            1204.
        size (Union[Unset, int]): Size is the archive's size as the storage announced it, and zero when it
            announced none - a client showing a percentage has to allow for that. Example: 3074211.
        started_at (Union[Unset, str]):
        state (Union[Unset, ArchiveRestoreState]):
    """

    deleted: Union[Unset, int] = UNSET
    downloaded: Union[Unset, int] = UNSET
    error: Union[Unset, str] = UNSET
    finished_at: Union[Unset, str] = UNSET
    restored: Union[Unset, int] = UNSET
    size: Union[Unset, int] = UNSET
    started_at: Union[Unset, str] = UNSET
    state: Union[Unset, ArchiveRestoreState] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deleted = self.deleted

        downloaded = self.downloaded

        error = self.error

        finished_at = self.finished_at

        restored = self.restored

        size = self.size

        started_at = self.started_at

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if downloaded is not UNSET:
            field_dict["downloaded"] = downloaded
        if error is not UNSET:
            field_dict["error"] = error
        if finished_at is not UNSET:
            field_dict["finishedAt"] = finished_at
        if restored is not UNSET:
            field_dict["restored"] = restored
        if size is not UNSET:
            field_dict["size"] = size
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        deleted = d.pop("deleted", UNSET)

        downloaded = d.pop("downloaded", UNSET)

        error = d.pop("error", UNSET)

        finished_at = d.pop("finishedAt", d.pop("finished_at", UNSET))

        restored = d.pop("restored", UNSET)

        size = d.pop("size", UNSET)

        started_at = d.pop("startedAt", d.pop("started_at", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, ArchiveRestoreState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ArchiveRestoreState(_state)

        restore_progress = cls(
            deleted=deleted,
            downloaded=downloaded,
            error=error,
            finished_at=finished_at,
            restored=restored,
            size=size,
            started_at=started_at,
            state=state,
        )

        restore_progress.additional_properties = d
        return restore_progress

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
