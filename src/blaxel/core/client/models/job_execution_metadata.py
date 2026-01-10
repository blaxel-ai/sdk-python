from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobExecutionMetadata")


@_attrs_define
class JobExecutionMetadata:
    """Job execution metadata

    Attributes:
        cluster (Union[Unset, str]): Cluster ID
        completed_at (Union[Unset, str]): Completion timestamp
        created_at (Union[Unset, str]): Creation timestamp
        deleted_at (Union[Unset, str]): Deletion timestamp
        expired_at (Union[Unset, str]): Expiration timestamp
        id (Union[Unset, str]): Execution ID Example: exec-abc123.
        job (Union[Unset, str]): Job name Example: data-processing-job.
        started_at (Union[Unset, str]): Start timestamp
        updated_at (Union[Unset, str]): Last update timestamp
        workspace (Union[Unset, str]): Workspace ID Example: my-workspace.
    """

    cluster: Union[Unset, str] = UNSET
    completed_at: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    deleted_at: Union[Unset, str] = UNSET
    expired_at: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    started_at: Union[Unset, str] = UNSET
    updated_at: Union[Unset, str] = UNSET
    workspace: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster = self.cluster

        completed_at = self.completed_at

        created_at = self.created_at

        deleted_at = self.deleted_at

        expired_at = self.expired_at

        id = self.id

        job = self.job

        started_at = self.started_at

        updated_at = self.updated_at

        workspace = self.workspace

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cluster is not UNSET:
            field_dict["cluster"] = cluster
        if completed_at is not UNSET:
            field_dict["completedAt"] = completed_at
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if expired_at is not UNSET:
            field_dict["expiredAt"] = expired_at
        if id is not UNSET:
            field_dict["id"] = id
        if job is not UNSET:
            field_dict["job"] = job
        if started_at is not UNSET:
            field_dict["startedAt"] = started_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if workspace is not UNSET:
            field_dict["workspace"] = workspace

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        cluster = d.pop("cluster", UNSET)

        completed_at = d.pop("completedAt", d.pop("completed_at", UNSET))

        created_at = d.pop("createdAt", d.pop("created_at", UNSET))

        deleted_at = d.pop("deletedAt", d.pop("deleted_at", UNSET))

        expired_at = d.pop("expiredAt", d.pop("expired_at", UNSET))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        started_at = d.pop("startedAt", d.pop("started_at", UNSET))

        updated_at = d.pop("updatedAt", d.pop("updated_at", UNSET))

        workspace = d.pop("workspace", UNSET)

        job_execution_metadata = cls(
            cluster=cluster,
            completed_at=completed_at,
            created_at=created_at,
            deleted_at=deleted_at,
            expired_at=expired_at,
            id=id,
            job=job,
            started_at=started_at,
            updated_at=updated_at,
            workspace=workspace,
        )

        job_execution_metadata.additional_properties = d
        return job_execution_metadata

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
