from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.function_runtime_generation import FunctionRuntimeGeneration
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.env import Env


T = TypeVar("T", bound="FunctionRuntime")


@_attrs_define
class FunctionRuntime:
    """Runtime configuration defining how the MCP server function is deployed and scaled

    Attributes:
        envs (Union[Unset, list['Env']]): Environment variables injected into the function. Supports Kubernetes EnvVar
            format with valueFrom references.
        generation (Union[Unset, FunctionRuntimeGeneration]): Infrastructure generation: mk2 (containers, 2-10s cold
            starts, 15+ global regions) or mk3 (microVMs, sub-25ms cold starts) Example: mk3.
        image (Union[Unset, str]): Container image built by Blaxel when deploying with 'bl deploy'. This field is auto-
            populated during deployment.
        max_scale (Union[Unset, int]): Maximum number of concurrent function instances for auto-scaling Example: 10.
        memory (Union[Unset, int]): Memory allocation in megabytes. Also determines CPU allocation (CPU cores = memory
            in MB / 2048, e.g., 4096MB = 2 CPUs). Example: 2048.
        min_scale (Union[Unset, int]): Minimum instances to keep warm. Set to 1+ to eliminate cold starts, 0 for scale-
            to-zero.
    """

    envs: Union[Unset, list["Env"]] = UNSET
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
        from ..models.env import Env

        if not src_dict:
            return None
        d = src_dict.copy()
        envs = []
        _envs = d.pop("envs", UNSET)
        for envs_item_data in _envs or []:
            envs_item = Env.from_dict(envs_item_data)

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
