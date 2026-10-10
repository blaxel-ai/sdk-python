from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateImageBody")


@_attrs_define
class CreateImageBody:
    """
    Attributes:
        name (str): Name of the image to build
        resource_type (str): Resource type (agent, function, sandbox, job)
        docker_config (Union[Unset, str]): Docker configuration JSON containing credentials for the source registry.
        generation (Union[Unset, str]): Runtime generation (e.g., mk3). Defaults to mk3 if not specified.
        image (Union[Unset, str]): A pre-built Docker image reference (e.g., docker.io/myorg/myimage:latest). References
            with a registry hostname start an asynchronous import that downloads and converts the image for the resource
            runtime.
        memory_mb (Union[Unset, int]): Memory for the registry import worker in MiB. Only supported when image is a
            registry reference. When omitted, the platform default is used. Example: 16384.
        volume_mb (Union[Unset, int]): Temporary scratch disk for the registry import worker in MiB. Only supported when
            image is a registry reference. When omitted, the platform default is used. Set to 0 to use memory-backed
            scratch. Positive values are not supported for HIPAA workspaces. Example: 32768.
    """

    name: str
    resource_type: str
    docker_config: Union[Unset, str] = UNSET
    generation: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    memory_mb: Union[Unset, int] = UNSET
    volume_mb: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        resource_type = self.resource_type

        docker_config = self.docker_config

        generation = self.generation

        image = self.image

        memory_mb = self.memory_mb

        volume_mb = self.volume_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resourceType": resource_type,
            }
        )
        if docker_config is not UNSET:
            field_dict["dockerConfig"] = docker_config
        if generation is not UNSET:
            field_dict["generation"] = generation
        if image is not UNSET:
            field_dict["image"] = image
        if memory_mb is not UNSET:
            field_dict["memoryMb"] = memory_mb
        if volume_mb is not UNSET:
            field_dict["volumeMb"] = volume_mb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T | None:
        if not src_dict:
            return None
        d = src_dict.copy()
        name = d.pop("name")

        resource_type = d.pop("resourceType") if "resourceType" in d else d.pop("resource_type")

        docker_config = d.pop("dockerConfig", d.pop("docker_config", UNSET))

        generation = d.pop("generation", UNSET)

        image = d.pop("image", UNSET)

        memory_mb = d.pop("memoryMb", d.pop("memory_mb", UNSET))

        volume_mb = d.pop("volumeMb", d.pop("volume_mb", UNSET))

        create_image_body = cls(
            name=name,
            resource_type=resource_type,
            docker_config=docker_config,
            generation=generation,
            image=image,
            memory_mb=memory_mb,
            volume_mb=volume_mb,
        )

        create_image_body.additional_properties = d
        return create_image_body

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
