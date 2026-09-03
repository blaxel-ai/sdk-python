from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.archive_quiesce_state import ArchiveQuiesceState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_progress import ExportProgress
    from ..models.restore_progress import RestoreProgress


T = TypeVar("T", bound="QuiesceStatus")


@_attrs_define
class QuiesceStatus:
    """
    Attributes:
        state (ArchiveQuiesceState):
        export (Union[Unset, ExportProgress]):
        read_only_root (Union[Unset, bool]): ReadOnlyRoot reports whether the root mount was remounted read-only, which
            is what actually stops writes; false means the freeze relies only on the
            API refusing calls, and the reason says why. Example: True.
        reason (Union[Unset, str]): Reason is a human readable explanation of why the sandbox is frozen. Example:
            archive export.
        restore (Union[Unset, RestoreProgress]):
        since (Union[Unset, str]): Since is when the sandbox left StateActive.
        stopped_processes (Union[Unset, list[str]]): StoppedProcesses are the process identifiers stopped while
            quiescing.
    """

    state: ArchiveQuiesceState
    export: Union[Unset, "ExportProgress"] = UNSET
    read_only_root: Union[Unset, bool] = UNSET
    reason: Union[Unset, str] = UNSET
    restore: Union[Unset, "RestoreProgress"] = UNSET
    since: Union[Unset, str] = UNSET
    stopped_processes: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        state = self.state.value

        export: Union[Unset, dict[str, Any]] = UNSET
        if self.export and not isinstance(self.export, Unset) and not isinstance(self.export, dict):
            export = self.export.to_dict()
        elif self.export and isinstance(self.export, dict):
            export = self.export

        read_only_root = self.read_only_root

        reason = self.reason

        restore: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.restore
            and not isinstance(self.restore, Unset)
            and not isinstance(self.restore, dict)
        ):
            restore = self.restore.to_dict()
        elif self.restore and isinstance(self.restore, dict):
            restore = self.restore

        since = self.since

        stopped_processes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.stopped_processes, Unset):
            stopped_processes = self.stopped_processes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
            }
        )
        if export is not UNSET:
            field_dict["export"] = export
        if read_only_root is not UNSET:
            field_dict["readOnlyRoot"] = read_only_root
        if reason is not UNSET:
            field_dict["reason"] = reason
        if restore is not UNSET:
            field_dict["restore"] = restore
        if since is not UNSET:
            field_dict["since"] = since
        if stopped_processes is not UNSET:
            field_dict["stoppedProcesses"] = stopped_processes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.export_progress import ExportProgress
        from ..models.restore_progress import RestoreProgress

        if not src_dict:
            return None
        d = src_dict.copy()
        state = ArchiveQuiesceState(d.pop("state"))

        _export = d.pop("export", UNSET)
        export: Union[Unset, ExportProgress]
        if isinstance(_export, Unset):
            export = UNSET
        else:
            export = ExportProgress.from_dict(_export)

        read_only_root = d.pop("readOnlyRoot", d.pop("read_only_root", UNSET))

        reason = d.pop("reason", UNSET)

        _restore = d.pop("restore", UNSET)
        restore: Union[Unset, RestoreProgress]
        if isinstance(_restore, Unset):
            restore = UNSET
        else:
            restore = RestoreProgress.from_dict(_restore)

        since = d.pop("since", UNSET)

        stopped_processes = cast(
            list[str], d.pop("stoppedProcesses", d.pop("stopped_processes", UNSET))
        )

        quiesce_status = cls(
            state=state,
            export=export,
            read_only_root=read_only_root,
            reason=reason,
            restore=restore,
            since=since,
            stopped_processes=stopped_processes,
        )

        quiesce_status.additional_properties = d
        return quiesce_status

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
