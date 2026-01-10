from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_execution_task_status import JobExecutionTaskStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_execution_task_condition import JobExecutionTaskCondition
    from ..models.job_execution_task_metadata import JobExecutionTaskMetadata
    from ..models.job_execution_task_spec import JobExecutionTaskSpec


T = TypeVar("T", bound="JobExecutionTask")


@_attrs_define
class JobExecutionTask:
    """Job execution task

    Attributes:
        conditions (Union[Unset, list['JobExecutionTaskCondition']]): Task conditions
        metadata (Union[Unset, JobExecutionTaskMetadata]): Job execution task metadata
        spec (Union[Unset, JobExecutionTaskSpec]): Job execution task specification
        status (Union[Unset, JobExecutionTaskStatus]): Job execution task status
    """

    conditions: Union[Unset, list["JobExecutionTaskCondition"]] = UNSET
    metadata: Union[Unset, "JobExecutionTaskMetadata"] = UNSET
    spec: Union[Unset, "JobExecutionTaskSpec"] = UNSET
    status: Union[Unset, JobExecutionTaskStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conditions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = []
            for conditions_item_data in self.conditions:
                if type(conditions_item_data) is dict:
                    conditions_item = conditions_item_data
                else:
                    conditions_item = conditions_item_data.to_dict()
                conditions.append(conditions_item)

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.metadata
            and not isinstance(self.metadata, Unset)
            and not isinstance(self.metadata, dict)
        ):
            metadata = self.metadata.to_dict()
        elif self.metadata and isinstance(self.metadata, dict):
            metadata = self.metadata

        spec: Union[Unset, dict[str, Any]] = UNSET
        if self.spec and not isinstance(self.spec, Unset) and not isinstance(self.spec, dict):
            spec = self.spec.to_dict()
        elif self.spec and isinstance(self.spec, dict):
            spec = self.spec

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if spec is not UNSET:
            field_dict["spec"] = spec
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.job_execution_task_condition import JobExecutionTaskCondition
        from ..models.job_execution_task_metadata import JobExecutionTaskMetadata
        from ..models.job_execution_task_spec import JobExecutionTaskSpec

        if not src_dict:
            return None
        d = src_dict.copy()
        conditions = []
        _conditions = d.pop("conditions", UNSET)
        for conditions_item_data in _conditions or []:
            conditions_item = JobExecutionTaskCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, JobExecutionTaskMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = JobExecutionTaskMetadata.from_dict(_metadata)

        _spec = d.pop("spec", UNSET)
        spec: Union[Unset, JobExecutionTaskSpec]
        if isinstance(_spec, Unset):
            spec = UNSET
        else:
            spec = JobExecutionTaskSpec.from_dict(_spec)

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobExecutionTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = JobExecutionTaskStatus(_status)

        job_execution_task = cls(
            conditions=conditions,
            metadata=metadata,
            spec=spec,
            status=status,
        )

        job_execution_task.additional_properties = d
        return job_execution_task

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
