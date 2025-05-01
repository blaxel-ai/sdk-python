from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.port import Port
    from ..models.runtime_configuration import RuntimeConfiguration
    from ..models.runtime_startup_probe import RuntimeStartupProbe


T = TypeVar("T", bound="Runtime")


@_attrs_define
class Runtime:
    """Set of configurations for a deployment

    Attributes:
        args (Union[Unset, list[Any]]): The arguments to pass to the deployment runtime
        command (Union[Unset, list[Any]]): The command to run the deployment
        configuration (Union[Unset, RuntimeConfiguration]): The configuration for the deployment
        cpu (Union[Unset, int]): The CPU for the deployment in cores, only available for private cluster
        endpoint_name (Union[Unset, str]): Endpoint Name of the model. In case of hf_private_endpoint, it is the
            endpoint name. In case of hf_public_endpoint, it is not used.
        envs (Union[Unset, list[Any]]): The env variables to set in the deployment. Should be a list of Kubernetes
            EnvVar types
        generation (Union[Unset, str]): The generation of the deployment
        image (Union[Unset, str]): The Docker image for the deployment
        max_scale (Union[Unset, int]): The minimum number of replicas for the deployment. Can be 0 or 1 (in which case
            the deployment is always running in at least one location).
        memory (Union[Unset, int]): The memory for the deployment in MB
        metric_port (Union[Unset, int]): The port to serve the metrics on
        min_scale (Union[Unset, int]): The maximum number of replicas for the deployment.
        model (Union[Unset, str]): The slug name of the origin model at HuggingFace.
        organization (Union[Unset, str]): The organization of the model
        ports (Union[Unset, list['Port']]): Set of ports for a resource
        startup_probe (Union[Unset, RuntimeStartupProbe]): The readiness probe. Should be a Kubernetes Probe type
        timeout (Union[Unset, int]): The timeout for the deployment in seconds
        type_ (Union[Unset, str]): The type of origin for the deployment (hf_private_endpoint, hf_public_endpoint)
    """

    args: Union[Unset, list[Any]] = UNSET
    command: Union[Unset, list[Any]] = UNSET
    configuration: Union[Unset, "RuntimeConfiguration"] = UNSET
    cpu: Union[Unset, int] = UNSET
    endpoint_name: Union[Unset, str] = UNSET
    envs: Union[Unset, list[Any]] = UNSET
    generation: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    max_scale: Union[Unset, int] = UNSET
    memory: Union[Unset, int] = UNSET
    metric_port: Union[Unset, int] = UNSET
    min_scale: Union[Unset, int] = UNSET
    model: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    ports: Union[Unset, list["Port"]] = UNSET
    startup_probe: Union[Unset, "RuntimeStartupProbe"] = UNSET
    timeout: Union[Unset, int] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        args: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        command: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        configuration: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.configuration
            and not isinstance(self.configuration, Unset)
            and not isinstance(self.configuration, dict)
        ):
            configuration = self.configuration.to_dict()
        elif self.configuration and isinstance(self.configuration, dict):
            configuration = self.configuration

        cpu = self.cpu

        endpoint_name = self.endpoint_name

        envs: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = self.envs

        generation = self.generation

        image = self.image

        max_scale = self.max_scale

        memory = self.memory

        metric_port = self.metric_port

        min_scale = self.min_scale

        model = self.model

        organization = self.organization

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for componentsschemas_ports_item_data in self.ports:
                if type(componentsschemas_ports_item_data) == dict:
                    componentsschemas_ports_item = componentsschemas_ports_item_data
                else:
                    componentsschemas_ports_item = componentsschemas_ports_item_data.to_dict()
                ports.append(componentsschemas_ports_item)

        startup_probe: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.startup_probe
            and not isinstance(self.startup_probe, Unset)
            and not isinstance(self.startup_probe, dict)
        ):
            startup_probe = self.startup_probe.to_dict()
        elif self.startup_probe and isinstance(self.startup_probe, dict):
            startup_probe = self.startup_probe

        timeout = self.timeout

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args
        if command is not UNSET:
            field_dict["command"] = command
        if configuration is not UNSET:
            field_dict["configuration"] = configuration
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if endpoint_name is not UNSET:
            field_dict["endpointName"] = endpoint_name
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
        if metric_port is not UNSET:
            field_dict["metricPort"] = metric_port
        if min_scale is not UNSET:
            field_dict["minScale"] = min_scale
        if model is not UNSET:
            field_dict["model"] = model
        if organization is not UNSET:
            field_dict["organization"] = organization
        if ports is not UNSET:
            field_dict["ports"] = ports
        if startup_probe is not UNSET:
            field_dict["startupProbe"] = startup_probe
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.port import Port
        from ..models.runtime_configuration import RuntimeConfiguration
        from ..models.runtime_startup_probe import RuntimeStartupProbe

        if not src_dict:
            return None
        d = src_dict.copy()
        args = cast(list[Any], d.pop("args", UNSET))

        command = cast(list[Any], d.pop("command", UNSET))

        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, RuntimeConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = RuntimeConfiguration.from_dict(_configuration)

        cpu = d.pop("cpu", UNSET)

        endpoint_name = d.pop("endpointName", UNSET)

        envs = cast(list[Any], d.pop("envs", UNSET))

        generation = d.pop("generation", UNSET)

        image = d.pop("image", UNSET)

        max_scale = d.pop("maxScale", UNSET)

        memory = d.pop("memory", UNSET)

        metric_port = d.pop("metricPort", UNSET)

        min_scale = d.pop("minScale", UNSET)

        model = d.pop("model", UNSET)

        organization = d.pop("organization", UNSET)

        ports = []
        _ports = d.pop("ports", UNSET)
        for componentsschemas_ports_item_data in _ports or []:
            componentsschemas_ports_item = Port.from_dict(componentsschemas_ports_item_data)

            ports.append(componentsschemas_ports_item)

        _startup_probe = d.pop("startupProbe", UNSET)
        startup_probe: Union[Unset, RuntimeStartupProbe]
        if isinstance(_startup_probe, Unset):
            startup_probe = UNSET
        else:
            startup_probe = RuntimeStartupProbe.from_dict(_startup_probe)

        timeout = d.pop("timeout", UNSET)

        type_ = d.pop("type", UNSET)

        runtime = cls(
            args=args,
            command=command,
            configuration=configuration,
            cpu=cpu,
            endpoint_name=endpoint_name,
            envs=envs,
            generation=generation,
            image=image,
            max_scale=max_scale,
            memory=memory,
            metric_port=metric_port,
            min_scale=min_scale,
            model=model,
            organization=organization,
            ports=ports,
            startup_probe=startup_probe,
            timeout=timeout,
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
