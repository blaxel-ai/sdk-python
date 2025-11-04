from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trigger_configuration_task import TriggerConfigurationTask


T = TypeVar("T", bound="TriggerConfiguration")


@_attrs_define
class TriggerConfiguration:
    """Trigger configuration

    Attributes:
        authentication_type (Union[Unset, str]): The authentication type of the trigger
        path (Union[Unset, str]): The path of the trigger
        retry (Union[Unset, int]): The retry of the trigger
        schedule (Union[Unset, str]): The schedule of the trigger, cron expression * * * * *
        tasks (Union[Unset, list['TriggerConfigurationTask']]): The tasks configuration of the cronjob
    """

    authentication_type: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    retry: Union[Unset, int] = UNSET
    schedule: Union[Unset, str] = UNSET
    tasks: Union[Unset, list["TriggerConfigurationTask"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        authentication_type = self.authentication_type

        path = self.path

        retry = self.retry

        schedule = self.schedule

        tasks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                if type(tasks_item_data) is dict:
                    tasks_item = tasks_item_data
                else:
                    tasks_item = tasks_item_data.to_dict()
                tasks.append(tasks_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if authentication_type is not UNSET:
            field_dict["authenticationType"] = authentication_type
        if path is not UNSET:
            field_dict["path"] = path
        if retry is not UNSET:
            field_dict["retry"] = retry
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.trigger_configuration_task import TriggerConfigurationTask

        if not src_dict:
            return None
        d = src_dict.copy()
        authentication_type = d.pop("authenticationType", UNSET)

        path = d.pop("path", UNSET)

        retry = d.pop("retry", UNSET)

        schedule = d.pop("schedule", UNSET)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = TriggerConfigurationTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        trigger_configuration = cls(
            authentication_type=authentication_type,
            path=path,
            retry=retry,
            schedule=schedule,
            tasks=tasks,
        )

        trigger_configuration.additional_properties = d
        return trigger_configuration

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
