from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.function_runtime_generation import FunctionRuntimeGeneration
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_runtime_envs_item import FunctionRuntimeEnvsItem


T = TypeVar("T", bound="FunctionRuntime")


@_attrs_define
class FunctionRuntime:
    """Runtime configuration for Function

    Attributes:
        envs (Union[Unset, list['FunctionRuntimeEnvsItem']]): The env variables to set in the function. Should be a list
            of Kubernetes EnvVar types
        generation (Union[Unset, FunctionRuntimeGeneration]): The generation of the function
        image (Union[Unset, str]): The Docker image for the function
        max_scale (Union[Unset, int]): The maximum number of replicas for the function.
        memory (Union[Unset, int]): The memory for the function in MB
        min_scale (Union[Unset, int]): The minimum number of replicas for the function. Can be 0 or 1 (in which case the
            function is always running in at least one location).
    """

    envs: Union[Unset, list["FunctionRuntimeEnvsItem"]] = UNSET
    generation: Union[Unset, FunctionRuntimeGeneration] = UNSET
    image: Union[Unset, str] = UNSET
    max_scale: Union[Unset, int] = UNSET
    memory: Union[Unset, int] = UNSET
    min_scale: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        envs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = []
            for envs_item_data in self.envs:
                if type(envs_item_data) is dict:
                    envs_item = envs_item_data
                else:
                    envs_item = envs_item_data.to_dict()
                envs.append(envs_item)

        generation: Union[Unset, str] = UNSET
        if not isinstance(self.generation, Unset):
            generation = self.generation.value

        image = self.image

        max_scale = self.max_scale

        memory = self.memory

        min_scale = self.min_scale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if envs is not UNSET:
            field_dict["envs"] = envs
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image
        if max_scale is not UNSET:
            field_dict["maxScale"] = max_scale
        if memory is not UNSET:
            field_dict["memory"] = memory
        if min_scale is not UNSET:
            field_dict["minScale"] = min_scale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        from ..models.function_runtime_envs_item import FunctionRuntimeEnvsItem

        if not src_dict:
            return None
        d = src_dict.copy()
        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = FunctionRuntimeEnvsItem.from_dict(envs_item_data)

            envs.append(envs_item)

        _generation = d.pop("generation", UNSET)
        generation: Union[Unset, FunctionRuntimeGeneration]
        if isinstance(_generation, Unset):
            generation = UNSET
        else:
            generation = FunctionRuntimeGeneration(_generation)

        image = d.pop("image", UNSET)

        max_scale = d.pop("maxScale", d.pop("max_scale", UNSET))

        memory = d.pop("memory", UNSET)

        min_scale = d.pop("minScale", d.pop("min_scale", UNSET))

        function_runtime = cls(
            envs=envs,
            generation=generation,
            image=image,
            max_scale=max_scale,
            memory=memory,
            min_scale=min_scale,
        )

        function_runtime.additional_properties = d
        return function_runtime

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
