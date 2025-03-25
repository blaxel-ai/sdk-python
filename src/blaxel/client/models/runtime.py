from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.runtime_startup_probe import RuntimeStartupProbe


T = TypeVar("T", bound="Runtime")


@_attrs_define
class Runtime:
    """Set of configurations for a deployment

    Attributes:
        args (Union[Unset, list[Any]]): The arguments to pass to the deployment runtime
        command (Union[Unset, list[Any]]): The command to run the deployment
        cpu (Union[Unset, int]): The CPU for the deployment in cores, only available for private cluster
        endpoint_name (Union[Unset, str]): Endpoint Name of the model. In case of hf_private_endpoint, it is the
            endpoint name. In case of hf_public_endpoint, it is not used.
        envs (Union[Unset, list[Any]]): The env variables to set in the deployment. Should be a list of Kubernetes
            EnvVar types
        image (Union[Unset, str]): The Docker image for the deployment
        memory (Union[Unset, int]): The memory for the deployment in MB
        metric_port (Union[Unset, int]): The port to serve the metrics on
        model (Union[Unset, str]): The slug name of the origin model at HuggingFace.
        organization (Union[Unset, str]): The organization of the model
        serving_port (Union[Unset, int]): The port to serve the model on
        startup_probe (Union[Unset, RuntimeStartupProbe]): The readiness probe. Should be a Kubernetes Probe type
        type_ (Union[Unset, str]): The type of origin for the deployment (hf_private_endpoint, hf_public_endpoint)
    """

    args: Union[Unset, list[Any]] = UNSET
    command: Union[Unset, list[Any]] = UNSET
    cpu: Union[Unset, int] = UNSET
    endpoint_name: Union[Unset, str] = UNSET
    envs: Union[Unset, list[Any]] = UNSET
    image: Union[Unset, str] = UNSET
    memory: Union[Unset, int] = UNSET
    metric_port: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    serving_port: Union[Unset, int] = UNSET
    startup_probe: Union[Unset, "RuntimeStartupProbe"] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        args: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        command: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        cpu = self.cpu

        endpoint_name = self.endpoint_name

        envs: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = self.envs

        image = self.image

        memory = self.memory

        metric_port = self.metric_port

        model = self.model

        organization = self.organization

        serving_port = self.serving_port

        startup_probe: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.startup_probe
            and not isinstance(self.startup_probe, Unset)
            and not isinstance(self.startup_probe, dict)
        ):
            startup_probe = self.startup_probe.to_dict()
        elif self.startup_probe and isinstance(self.startup_probe, dict):
            startup_probe = self.startup_probe

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if command is not UNSET:
            field_dict["command"] = command
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if endpoint_name is not UNSET:
            field_dict["endpointName"] = endpoint_name
        if envs is not UNSET:
            field_dict["envs"] = envs
        if image is not UNSET:
            field_dict["image"] = image
        if memory is not UNSET:
            field_dict["memory"] = memory
        if metric_port is not UNSET:
            field_dict["metricPort"] = metric_port
        if model is not UNSET:
            field_dict["model"] = model
        if organization is not UNSET:
            field_dict["organization"] = organization
        if serving_port is not UNSET:
            field_dict["servingPort"] = serving_port
        if startup_probe is not UNSET:
            field_dict["startupProbe"] = startup_probe
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.runtime_startup_probe import RuntimeStartupProbe

        if not src_dict:
            return None
        d = src_dict.copy()
        args = cast(list[Any], d.pop("args", UNSET))

        command = cast(list[Any], d.pop("command", UNSET))

        cpu = d.pop("cpu", UNSET)

        endpoint_name = d.pop("endpointName", UNSET)

        envs = cast(list[Any], d.pop("envs", UNSET))

        image = d.pop("image", UNSET)

        memory = d.pop("memory", UNSET)

        metric_port = d.pop("metricPort", UNSET)

        model = d.pop("model", UNSET)

        organization = d.pop("organization", UNSET)

        serving_port = d.pop("servingPort", UNSET)

        _startup_probe = d.pop("startupProbe", UNSET)
        startup_probe: Union[Unset, RuntimeStartupProbe]
        if isinstance(_startup_probe, Unset):
            startup_probe = UNSET
        else:
            startup_probe = RuntimeStartupProbe.from_dict(_startup_probe)

        type_ = d.pop("type", UNSET)

        runtime = cls(
            args=args,
            command=command,
            cpu=cpu,
            endpoint_name=endpoint_name,
            envs=envs,
            image=image,
            memory=memory,
            metric_port=metric_port,
            model=model,
            organization=organization,
            serving_port=serving_port,
            startup_probe=startup_probe,
            type_=type_,
        )

        runtime.additional_properties = d
        return runtime

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
