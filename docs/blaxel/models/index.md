Module blaxel.models
====================
Contains all the data models used in inputs/outputs

Sub-modules
-----------
* blaxel.models.acl
* blaxel.models.agent
* blaxel.models.agent_chain
* blaxel.models.agent_spec
* blaxel.models.api_key
* blaxel.models.configuration
* blaxel.models.continent
* blaxel.models.core_event
* blaxel.models.core_spec
* blaxel.models.core_spec_configurations
* blaxel.models.country
* blaxel.models.create_api_key_for_service_account_body
* blaxel.models.create_workspace_service_account_body
* blaxel.models.create_workspace_service_account_response_200
* blaxel.models.delete_workspace_service_account_response_200
* blaxel.models.entrypoint
* blaxel.models.entrypoint_env
* blaxel.models.flavor
* blaxel.models.form
* blaxel.models.form_config
* blaxel.models.form_oauth
* blaxel.models.form_secrets
* blaxel.models.function
* blaxel.models.function_kit
* blaxel.models.function_schema
* blaxel.models.function_schema_not
* blaxel.models.function_schema_or_bool
* blaxel.models.function_schema_properties
* blaxel.models.function_spec
* blaxel.models.get_workspace_service_accounts_response_200_item
* blaxel.models.histogram_bucket
* blaxel.models.histogram_stats
* blaxel.models.integration_connection
* blaxel.models.integration_connection_spec
* blaxel.models.integration_connection_spec_config
* blaxel.models.integration_connection_spec_secret
* blaxel.models.integration_model
* blaxel.models.integration_repository
* blaxel.models.invite_workspace_user_body
* blaxel.models.knowledgebase
* blaxel.models.knowledgebase_spec
* blaxel.models.knowledgebase_spec_options
* blaxel.models.last_n_requests_metric
* blaxel.models.latency_metric
* blaxel.models.location_response
* blaxel.models.mcp_definition
* blaxel.models.mcp_definition_entrypoint
* blaxel.models.mcp_definition_form
* blaxel.models.memory_allocation_metric
* blaxel.models.metadata
* blaxel.models.metadata_labels
* blaxel.models.metric
* blaxel.models.metrics
* blaxel.models.metrics_models
* blaxel.models.metrics_request_total_per_code
* blaxel.models.metrics_rps_per_code
* blaxel.models.model
* blaxel.models.model_private_cluster
* blaxel.models.model_spec
* blaxel.models.o_auth
* blaxel.models.owner_fields
* blaxel.models.pending_invitation
* blaxel.models.pending_invitation_accept
* blaxel.models.pending_invitation_render
* blaxel.models.pending_invitation_render_invited_by
* blaxel.models.pending_invitation_render_workspace
* blaxel.models.pending_invitation_workspace_details
* blaxel.models.pod_template_spec
* blaxel.models.policy
* blaxel.models.policy_location
* blaxel.models.policy_max_tokens
* blaxel.models.policy_spec
* blaxel.models.private_cluster
* blaxel.models.private_location
* blaxel.models.repository
* blaxel.models.request_duration_over_time_metric
* blaxel.models.request_duration_over_time_metrics
* blaxel.models.request_total_by_origin_metric
* blaxel.models.request_total_by_origin_metric_request_total_by_origin
* blaxel.models.request_total_by_origin_metric_request_total_by_origin_and_code
* blaxel.models.request_total_metric
* blaxel.models.request_total_metric_request_total_per_code
* blaxel.models.request_total_metric_rps_per_code
* blaxel.models.resource_log
* blaxel.models.resource_metrics
* blaxel.models.resource_metrics_request_total_per_code
* blaxel.models.resource_metrics_rps_per_code
* blaxel.models.revision_configuration
* blaxel.models.revision_metadata
* blaxel.models.runtime
* blaxel.models.runtime_startup_probe
* blaxel.models.serverless_config
* blaxel.models.spec_configuration
* blaxel.models.store_agent
* blaxel.models.store_agent_labels
* blaxel.models.store_configuration
* blaxel.models.store_configuration_option
* blaxel.models.template
* blaxel.models.template_variable
* blaxel.models.time_fields
* blaxel.models.time_to_first_token_over_time_metrics
* blaxel.models.token_rate_metric
* blaxel.models.token_rate_metrics
* blaxel.models.token_total_metric
* blaxel.models.trace_ids_response
* blaxel.models.update_workspace_service_account_body
* blaxel.models.update_workspace_service_account_response_200
* blaxel.models.update_workspace_user_role_body
* blaxel.models.websocket_channel
* blaxel.models.workspace
* blaxel.models.workspace_labels
* blaxel.models.workspace_user

Classes
-------

`ACL(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, id: blaxel.types.Unset | str = <blaxel.types.Unset object>, resource_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, resource_type: blaxel.types.Unset | str = <blaxel.types.Unset object>, role: blaxel.types.Unset | str = <blaxel.types.Unset object>, subject_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, subject_type: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   ACL
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        id (Union[Unset, str]): ACL id
        resource_id (Union[Unset, str]): Resource ID
        resource_type (Union[Unset, str]): Resource type
        role (Union[Unset, str]): Role
        subject_id (Union[Unset, str]): Subject ID
        subject_type (Union[Unset, str]): Subject type
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class ACL.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `id: blaxel.types.Unset | str`
    :

    `resource_id: blaxel.types.Unset | str`
    :

    `resource_type: blaxel.types.Unset | str`
    :

    `role: blaxel.types.Unset | str`
    :

    `subject_id: blaxel.types.Unset | str`
    :

    `subject_type: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    `workspace: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Agent(events: blaxel.types.Unset | list['CoreEvent'] = <blaxel.types.Unset object>, metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('AgentSpec') = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Agent
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, AgentSpec]): Agent specification
        status (Union[Unset, str]): Agent status
    
    Method generated by attrs for class Agent.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`AgentChain(description: blaxel.types.Unset | str = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, prompt: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Agent chain configuration
    
    Attributes:
        description (Union[Unset, str]): Description of the agent in case you want to override the default one
        enabled (Union[Unset, bool]): Whether the agent chain is enabled
        name (Union[Unset, str]): The name of the agent to chain to
        prompt (Union[Unset, str]): Prompt of the agent in case you want to override the default one
    
    Method generated by attrs for class AgentChain.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `description: blaxel.types.Unset | str`
    :

    `enabled: blaxel.types.Unset | bool`
    :

    `name: blaxel.types.Unset | str`
    :

    `prompt: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`AgentSpec(configurations: blaxel.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, integration_connections: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, pod_template: blaxel.types.Unset | ForwardRef('PodTemplateSpec') = <blaxel.types.Unset object>, policies: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, private_clusters: blaxel.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.types.Unset object>, revision: blaxel.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.types.Unset object>, runtime: blaxel.types.Unset | ForwardRef('Runtime') = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, serverless_config: blaxel.types.Unset | ForwardRef('ServerlessConfig') = <blaxel.types.Unset object>, agent_chain: blaxel.types.Unset | list['AgentChain'] = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, functions: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, knowledgebase: blaxel.types.Unset | str = <blaxel.types.Unset object>, model: blaxel.types.Unset | str = <blaxel.types.Unset object>, prompt: blaxel.types.Unset | str = <blaxel.types.Unset object>, repository: blaxel.types.Unset | ForwardRef('Repository') = <blaxel.types.Unset object>, store_id: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Agent specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the agent
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        pod_template (Union[Unset, PodTemplateSpec]): Pod template specification
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        serverless_config (Union[Unset, ServerlessConfig]): Configuration for a serverless deployment
        agent_chain (Union[Unset, list['AgentChain']]): Agent chain
        description (Union[Unset, str]): Description, small description computed from the prompt
        functions (Union[Unset, list[str]]):
        knowledgebase (Union[Unset, str]): Knowledgebase Name
        model (Union[Unset, str]): Model name
        prompt (Union[Unset, str]): Prompt, describe what your agent does
        repository (Union[Unset, Repository]): Repository
        store_id (Union[Unset, str]): Store id
    
    Method generated by attrs for class AgentSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `agent_chain`
    :

    `configurations`
    :

    `description`
    :

    `enabled`
    :

    `flavors`
    :

    `functions`
    :

    `integration_connections`
    :

    `knowledgebase`
    :

    `model`
    :

    `pod_template`
    :

    `policies`
    :

    `private_clusters`
    :

    `prompt`
    :

    `repository`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `serverless_config`
    :

    `store_id`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ApiKey(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, api_key: blaxel.types.Unset | str = <blaxel.types.Unset object>, expires_in: blaxel.types.Unset | str = <blaxel.types.Unset object>, id: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, sub: blaxel.types.Unset | str = <blaxel.types.Unset object>, sub_type: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Long-lived API key for accessing Blaxel
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        api_key (Union[Unset, str]): Api key
        expires_in (Union[Unset, str]): Duration until expiration (in seconds)
        id (Union[Unset, str]): Api key id, to retrieve it from the API
        name (Union[Unset, str]): Name for the API key
        sub (Union[Unset, str]): User subject identifier
        sub_type (Union[Unset, str]): Subject type
    
    Method generated by attrs for class ApiKey.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `api_key: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `created_by: blaxel.types.Unset | str`
    :

    `expires_in: blaxel.types.Unset | str`
    :

    `id: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `sub: blaxel.types.Unset | str`
    :

    `sub_type: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    `updated_by: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Configuration(continents: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, countries: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, private_locations: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>)`
:   Configuration
    
    Attributes:
        continents (Union[Unset, list[Any]]): Continents
        countries (Union[Unset, list[Any]]): Countries
        private_locations (Union[Unset, list[Any]]): Private locations managed with blaxel operator
    
    Method generated by attrs for class Configuration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `continents: blaxel.types.Unset | list[typing.Any]`
    :

    `countries: blaxel.types.Unset | list[typing.Any]`
    :

    `private_locations: blaxel.types.Unset | list[typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Continent(display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Continent
    
    Attributes:
        display_name (Union[Unset, str]): Continent display name
        name (Union[Unset, str]): Continent code
    
    Method generated by attrs for class Continent.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `display_name: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreEvent(message: blaxel.types.Unset | str = <blaxel.types.Unset object>, revision: blaxel.types.Unset | str = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>, time: blaxel.types.Unset | str = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Core event
    
    Attributes:
        message (Union[Unset, str]): Event message
        revision (Union[Unset, str]): RevisionID link to the event
        status (Union[Unset, str]): Event status
        time (Union[Unset, str]): Event time
        type_ (Union[Unset, str]): Event type
    
    Method generated by attrs for class CoreEvent.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `message: blaxel.types.Unset | str`
    :

    `revision: blaxel.types.Unset | str`
    :

    `status: blaxel.types.Unset | str`
    :

    `time: blaxel.types.Unset | str`
    :

    `type_: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreSpec(configurations: blaxel.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, integration_connections: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, pod_template: blaxel.types.Unset | ForwardRef('PodTemplateSpec') = <blaxel.types.Unset object>, policies: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, private_clusters: blaxel.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.types.Unset object>, revision: blaxel.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.types.Unset object>, runtime: blaxel.types.Unset | ForwardRef('Runtime') = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, serverless_config: blaxel.types.Unset | ForwardRef('ServerlessConfig') = <blaxel.types.Unset object>)`
:   Core specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the agent
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        pod_template (Union[Unset, PodTemplateSpec]): Pod template specification
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        serverless_config (Union[Unset, ServerlessConfig]): Configuration for a serverless deployment
    
    Method generated by attrs for class CoreSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `configurations`
    :

    `enabled`
    :

    `flavors`
    :

    `integration_connections`
    :

    `pod_template`
    :

    `policies`
    :

    `private_clusters`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `serverless_config`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreSpecConfigurations(key: blaxel.types.Unset | ForwardRef('SpecConfiguration') = <blaxel.types.Unset object>)`
:   Optional configurations for the object
    
    Attributes:
        key (Union[Unset, SpecConfiguration]): Configuration, this is a key value storage. In your object you can
            retrieve the value with config[key]
    
    Method generated by attrs for class CoreSpecConfigurations.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `key`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Country(display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Configuration
    
    Attributes:
        display_name (Union[Unset, str]): Country display name
        name (Union[Unset, str]): Country code
    
    Method generated by attrs for class Country.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `display_name: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateApiKeyForServiceAccountBody(expires_in: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        expires_in (Union[Unset, str]): Expiration period for the API key
        name (Union[Unset, str]): Name for the API key
    
    Method generated by attrs for class CreateApiKeyForServiceAccountBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `expires_in: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateWorkspaceServiceAccountBody(name: str, description: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        name (str): Service account name
        description (Union[Unset, str]): Service account description
    
    Method generated by attrs for class CreateWorkspaceServiceAccountBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateWorkspaceServiceAccountResponse200(client_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, client_secret: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        client_id (Union[Unset, str]): Service account client ID
        client_secret (Union[Unset, str]): Service account client secret (only returned on creation)
        created_at (Union[Unset, str]): Creation timestamp
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        updated_at (Union[Unset, str]): Last update timestamp
    
    Method generated by attrs for class CreateWorkspaceServiceAccountResponse200.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `client_id: blaxel.types.Unset | str`
    :

    `client_secret: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`DeleteWorkspaceServiceAccountResponse200(client_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        client_id (Union[Unset, str]): Service account client ID
        created_at (Union[Unset, str]): Creation timestamp
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        updated_at (Union[Unset, str]): Last update timestamp
    
    Method generated by attrs for class DeleteWorkspaceServiceAccountResponse200.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `client_id: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Entrypoint(args: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, command: blaxel.types.Unset | str = <blaxel.types.Unset object>, env: blaxel.types.Unset | ForwardRef('EntrypointEnv') = <blaxel.types.Unset object>)`
:   Entrypoint of the artifact
    
    Attributes:
        args (Union[Unset, list[Any]]): Args of the entrypoint
        command (Union[Unset, str]): Command of the entrypoint
        env (Union[Unset, EntrypointEnv]): Env of the entrypoint
    
    Method generated by attrs for class Entrypoint.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `args`
    :

    `command`
    :

    `env`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`EntrypointEnv()`
:   Env of the entrypoint
    
    Method generated by attrs for class EntrypointEnv.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Flavor(name: blaxel.types.Unset | str = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   A type of hardware available for deployments
    
    Attributes:
        name (Union[Unset, str]): Flavor name (e.g. t4)
        type_ (Union[Unset, str]): Flavor type (e.g. cpu, gpu)
    
    Method generated by attrs for class Flavor.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: blaxel.types.Unset | str`
    :

    `type_: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Form(config: blaxel.types.Unset | ForwardRef('FormConfig') = <blaxel.types.Unset object>, oauth: blaxel.types.Unset | ForwardRef('FormOauth') = <blaxel.types.Unset object>, secrets: blaxel.types.Unset | ForwardRef('FormSecrets') = <blaxel.types.Unset object>)`
:   Form of the artifact
    
    Attributes:
        config (Union[Unset, FormConfig]): Config of the artifact
        oauth (Union[Unset, FormOauth]): OAuth of the artifact
        secrets (Union[Unset, FormSecrets]): Secrets of the artifact
    
    Method generated by attrs for class Form.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `config`
    :

    `oauth`
    :

    `secrets`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FormConfig()`
:   Config of the artifact
    
    Method generated by attrs for class FormConfig.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FormOauth()`
:   OAuth of the artifact
    
    Method generated by attrs for class FormOauth.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FormSecrets()`
:   Secrets of the artifact
    
    Method generated by attrs for class FormSecrets.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Function(events: blaxel.types.Unset | list['CoreEvent'] = <blaxel.types.Unset object>, metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('FunctionSpec') = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Function
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, FunctionSpec]): Function specification
        status (Union[Unset, str]): Function status
    
    Method generated by attrs for class Function.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionKit(description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, schema: blaxel.types.Unset | ForwardRef('FunctionSchema') = <blaxel.types.Unset object>)`
:   Function kit
    
    Attributes:
        description (Union[Unset, str]): Description of the function kit, very important for the agent to work with your
            kit
        name (Union[Unset, str]): The kit name, very important for the agent to work with your kit
        schema (Union[Unset, FunctionSchema]): Function schema
    
    Method generated by attrs for class FunctionKit.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `description`
    :

    `name`
    :

    `schema`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionSchema(all_of: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, any_of: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, enum: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, format_: blaxel.types.Unset | str = <blaxel.types.Unset object>, items: blaxel.types.Unset | ForwardRef('FunctionSchema') = <blaxel.types.Unset object>, max_length: blaxel.types.Unset | float = <blaxel.types.Unset object>, maximum: blaxel.types.Unset | float = <blaxel.types.Unset object>, min_length: blaxel.types.Unset | float = <blaxel.types.Unset object>, minimum: blaxel.types.Unset | float = <blaxel.types.Unset object>, not_: blaxel.types.Unset | ForwardRef('FunctionSchemaNot') = <blaxel.types.Unset object>, one_of: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, pattern: blaxel.types.Unset | str = <blaxel.types.Unset object>, properties: blaxel.types.Unset | ForwardRef('FunctionSchemaProperties') = <blaxel.types.Unset object>, required: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, title: blaxel.types.Unset | str = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Function schema
    
    Attributes:
        all_of (Union[Unset, list[Any]]): List of schemas that this schema extends
        any_of (Union[Unset, list[Any]]): List of possible schemas, any of which this schema could be
        description (Union[Unset, str]): Description of the schema
        enum (Union[Unset, list[str]]): Enum values
        format_ (Union[Unset, str]): Format of the schema
        items (Union[Unset, FunctionSchema]): Function schema
        max_length (Union[Unset, float]): Maximum length for string types
        maximum (Union[Unset, float]): Maximum value for number types
        min_length (Union[Unset, float]): Minimum length for string types
        minimum (Union[Unset, float]): Minimum value for number types
        not_ (Union[Unset, FunctionSchemaNot]): Schema that this schema must not be
        one_of (Union[Unset, list[Any]]): List of schemas, one of which this schema must be
        pattern (Union[Unset, str]): Pattern for string types
        properties (Union[Unset, FunctionSchemaProperties]): Properties of the schema
        required (Union[Unset, list[str]]): Required properties of the schema
        title (Union[Unset, str]): Title of the schema
        type_ (Union[Unset, str]): Type of the schema
    
    Method generated by attrs for class FunctionSchema.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `all_of`
    :

    `any_of`
    :

    `description`
    :

    `enum`
    :

    `format_`
    :

    `items`
    :

    `max_length`
    :

    `maximum`
    :

    `min_length`
    :

    `minimum`
    :

    `not_`
    :

    `one_of`
    :

    `pattern`
    :

    `properties`
    :

    `required`
    :

    `title`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionSchemaNot()`
:   Schema that this schema must not be
    
    Method generated by attrs for class FunctionSchemaNot.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionSchemaOrBool()`
:   Helper type for AdditionalProperties which can be either a boolean or a schema
    
    Method generated by attrs for class FunctionSchemaOrBool.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionSchemaProperties()`
:   Properties of the schema
    
    Method generated by attrs for class FunctionSchemaProperties.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`FunctionSpec(configurations: blaxel.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, integration_connections: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, pod_template: blaxel.types.Unset | ForwardRef('PodTemplateSpec') = <blaxel.types.Unset object>, policies: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, private_clusters: blaxel.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.types.Unset object>, revision: blaxel.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.types.Unset object>, runtime: blaxel.types.Unset | ForwardRef('Runtime') = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, serverless_config: blaxel.types.Unset | ForwardRef('ServerlessConfig') = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, kit: blaxel.types.Unset | list['FunctionKit'] = <blaxel.types.Unset object>, schema: blaxel.types.Unset | ForwardRef('FunctionSchema') = <blaxel.types.Unset object>)`
:   Function specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the agent
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        pod_template (Union[Unset, PodTemplateSpec]): Pod template specification
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        serverless_config (Union[Unset, ServerlessConfig]): Configuration for a serverless deployment
        description (Union[Unset, str]): Function description, very important for the agent function to work with an LLM
        kit (Union[Unset, list['FunctionKit']]): Function kits
        schema (Union[Unset, FunctionSchema]): Function schema
    
    Method generated by attrs for class FunctionSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `configurations`
    :

    `description`
    :

    `enabled`
    :

    `flavors`
    :

    `integration_connections`
    :

    `kit`
    :

    `pod_template`
    :

    `policies`
    :

    `private_clusters`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `schema`
    :

    `serverless_config`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`GetWorkspaceServiceAccountsResponse200Item(client_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        client_id (Union[Unset, str]): Service account client ID
        created_at (Union[Unset, str]): Creation timestamp
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        updated_at (Union[Unset, str]): Last update timestamp
    
    Method generated by attrs for class GetWorkspaceServiceAccountsResponse200Item.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `client_id: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`HistogramBucket(count: blaxel.types.Unset | int = <blaxel.types.Unset object>, end: blaxel.types.Unset | float = <blaxel.types.Unset object>, start: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Histogram bucket
    
    Attributes:
        count (Union[Unset, int]): Count
        end (Union[Unset, float]): End
        start (Union[Unset, float]): Start
    
    Method generated by attrs for class HistogramBucket.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `count: blaxel.types.Unset | int`
    :

    `end: blaxel.types.Unset | float`
    :

    `start: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`HistogramStats(average: blaxel.types.Unset | float = <blaxel.types.Unset object>, p50: blaxel.types.Unset | float = <blaxel.types.Unset object>, p90: blaxel.types.Unset | float = <blaxel.types.Unset object>, p99: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Histogram stats
    
    Attributes:
        average (Union[Unset, float]): Average request duration
        p50 (Union[Unset, float]): P50 request duration
        p90 (Union[Unset, float]): P90 request duration
        p99 (Union[Unset, float]): P99 request duration
    
    Method generated by attrs for class HistogramStats.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `average: blaxel.types.Unset | float`
    :

    `p50: blaxel.types.Unset | float`
    :

    `p90: blaxel.types.Unset | float`
    :

    `p99: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationConnection(metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('IntegrationConnectionSpec') = <blaxel.types.Unset object>)`
:   Integration Connection
    
    Attributes:
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, IntegrationConnectionSpec]): Integration connection specification
    
    Method generated by attrs for class IntegrationConnection.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `metadata`
    :

    `spec`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationConnectionSpec(config: blaxel.types.Unset | ForwardRef('IntegrationConnectionSpecConfig') = <blaxel.types.Unset object>, integration: blaxel.types.Unset | str = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, secret: blaxel.types.Unset | ForwardRef('IntegrationConnectionSpecSecret') = <blaxel.types.Unset object>)`
:   Integration connection specification
    
    Attributes:
        config (Union[Unset, IntegrationConnectionSpecConfig]): Additional configuration for the integration
        integration (Union[Unset, str]): Integration type
        sandbox (Union[Unset, bool]): Sandbox mode
        secret (Union[Unset, IntegrationConnectionSpecSecret]): Integration secret
    
    Method generated by attrs for class IntegrationConnectionSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `config`
    :

    `integration`
    :

    `sandbox`
    :

    `secret`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationConnectionSpecConfig()`
:   Additional configuration for the integration
    
    Method generated by attrs for class IntegrationConnectionSpecConfig.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, str]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationConnectionSpecSecret()`
:   Integration secret
    
    Method generated by attrs for class IntegrationConnectionSpecSecret.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, str]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationModel(author: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, downloads: blaxel.types.Unset | int = <blaxel.types.Unset object>, endpoint: blaxel.types.Unset | str = <blaxel.types.Unset object>, id: blaxel.types.Unset | str = <blaxel.types.Unset object>, library_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, likes: blaxel.types.Unset | int = <blaxel.types.Unset object>, model_private: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, pipeline_tag: blaxel.types.Unset | str = <blaxel.types.Unset object>, tags: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, trending_score: blaxel.types.Unset | int = <blaxel.types.Unset object>)`
:   Model obtained from an external authentication provider, such as HuggingFace, OpenAI, etc...
    
    Attributes:
        author (Union[Unset, str]): Provider model author
        created_at (Union[Unset, str]): Provider model created at
        downloads (Union[Unset, int]): Provider model downloads
        endpoint (Union[Unset, str]): Model endpoint URL
        id (Union[Unset, str]): Provider model ID
        library_name (Union[Unset, str]): Provider model library name
        likes (Union[Unset, int]): Provider model likes
        model_private (Union[Unset, str]): Is the model private
        name (Union[Unset, str]): Provider model name
        pipeline_tag (Union[Unset, str]): Provider model pipeline tag
        tags (Union[Unset, list[str]]): Provider model tags
        trending_score (Union[Unset, int]): Provider model trending score
    
    Method generated by attrs for class IntegrationModel.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `author: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `downloads: blaxel.types.Unset | int`
    :

    `endpoint: blaxel.types.Unset | str`
    :

    `id: blaxel.types.Unset | str`
    :

    `library_name: blaxel.types.Unset | str`
    :

    `likes: blaxel.types.Unset | int`
    :

    `model_private: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `pipeline_tag: blaxel.types.Unset | str`
    :

    `tags: blaxel.types.Unset | list[str]`
    :

    `trending_score: blaxel.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationRepository(id: blaxel.types.Unset | str = <blaxel.types.Unset object>, is_bl: blaxel.types.Unset | bool = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, organization: blaxel.types.Unset | str = <blaxel.types.Unset object>, url: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Integration repository
    
    Attributes:
        id (Union[Unset, str]): Repository ID
        is_bl (Union[Unset, bool]): Whether the repository has Blaxel imports
        name (Union[Unset, str]): Repository name
        organization (Union[Unset, str]): Repository owner
        url (Union[Unset, str]): Repository URL
    
    Method generated by attrs for class IntegrationRepository.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `id: blaxel.types.Unset | str`
    :

    `is_bl: blaxel.types.Unset | bool`
    :

    `name: blaxel.types.Unset | str`
    :

    `organization: blaxel.types.Unset | str`
    :

    `url: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`InviteWorkspaceUserBody(email: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        email (Union[Unset, str]):
    
    Method generated by attrs for class InviteWorkspaceUserBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `email: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Knowledgebase(events: blaxel.types.Unset | list['CoreEvent'] = <blaxel.types.Unset object>, metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('KnowledgebaseSpec') = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Knowledgebase
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, KnowledgebaseSpec]): Knowledgebase specification
        status (Union[Unset, str]): Knowledgebase status
    
    Method generated by attrs for class Knowledgebase.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`KnowledgebaseSpec(collection_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, embedding_model: blaxel.types.Unset | str = <blaxel.types.Unset object>, embedding_model_type: blaxel.types.Unset | str = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, integration_connections: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, options: blaxel.types.Unset | ForwardRef('KnowledgebaseSpecOptions') = <blaxel.types.Unset object>, policies: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, revision: blaxel.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>)`
:   Knowledgebase specification
    
    Attributes:
        collection_name (Union[Unset, str]): Collection name
        embedding_model (Union[Unset, str]): Embedding model
        embedding_model_type (Union[Unset, str]): Embedding model type
        enabled (Union[Unset, bool]): Enable or disable the agent
        integration_connections (Union[Unset, list[str]]):
        options (Union[Unset, KnowledgebaseSpecOptions]): Options specific to the knowledge base
        policies (Union[Unset, list[str]]):
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        sandbox (Union[Unset, bool]): Sandbox mode
    
    Method generated by attrs for class KnowledgebaseSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `collection_name`
    :

    `embedding_model`
    :

    `embedding_model_type`
    :

    `enabled`
    :

    `integration_connections`
    :

    `options`
    :

    `policies`
    :

    `revision`
    :

    `sandbox`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`KnowledgebaseSpecOptions()`
:   Options specific to the knowledge base
    
    Method generated by attrs for class KnowledgebaseSpecOptions.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, str]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LastNRequestsMetric(date: blaxel.types.Unset | str = <blaxel.types.Unset object>, workload_type: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Last N requests
    
    Attributes:
        date (Union[Unset, str]): Timestamp
        workload_type (Union[Unset, str]): Workload type
        workspace (Union[Unset, str]): Workspace
    
    Method generated by attrs for class LastNRequestsMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `date: blaxel.types.Unset | str`
    :

    `workload_type: blaxel.types.Unset | str`
    :

    `workspace: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LatencyMetric(global_histogram: blaxel.types.Unset | ForwardRef('HistogramBucket') = <blaxel.types.Unset object>, global_stats: blaxel.types.Unset | ForwardRef('HistogramStats') = <blaxel.types.Unset object>, histogram_per_code: blaxel.types.Unset | ForwardRef('HistogramBucket') = <blaxel.types.Unset object>, stats_per_code: blaxel.types.Unset | ForwardRef('HistogramStats') = <blaxel.types.Unset object>)`
:   Latency metrics
    
    Attributes:
        global_histogram (Union[Unset, HistogramBucket]): Histogram bucket
        global_stats (Union[Unset, HistogramStats]): Histogram stats
        histogram_per_code (Union[Unset, HistogramBucket]): Histogram bucket
        stats_per_code (Union[Unset, HistogramStats]): Histogram stats
    
    Method generated by attrs for class LatencyMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `global_histogram`
    :

    `global_stats`
    :

    `histogram_per_code`
    :

    `stats_per_code`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LocationResponse(continent: blaxel.types.Unset | str = <blaxel.types.Unset object>, country: blaxel.types.Unset | str = <blaxel.types.Unset object>, flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, location: blaxel.types.Unset | str = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Location availability for policies
    
    Attributes:
        continent (Union[Unset, str]): Continent of the location
        country (Union[Unset, str]): Country of the location
        flavors (Union[Unset, list['Flavor']]): Hardware flavors available in the location
        location (Union[Unset, str]): Name of the location
        status (Union[Unset, str]): Status of the location
    
    Method generated by attrs for class LocationResponse.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `continent`
    :

    `country`
    :

    `flavors`
    :

    `location`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MCPDefinition(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, categories: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, coming_soon: blaxel.types.Unset | bool = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, enterprise: blaxel.types.Unset | bool = <blaxel.types.Unset object>, entrypoint: blaxel.types.Unset | ForwardRef('MCPDefinitionEntrypoint') = <blaxel.types.Unset object>, form: blaxel.types.Unset | ForwardRef('MCPDefinitionForm') = <blaxel.types.Unset object>, hidden_secrets: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, icon: blaxel.types.Unset | str = <blaxel.types.Unset object>, image: blaxel.types.Unset | str = <blaxel.types.Unset object>, integration: blaxel.types.Unset | str = <blaxel.types.Unset object>, long_description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, url: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Definition of an MCP from the MCP Hub
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        categories (Union[Unset, list[Any]]): Categories of the artifact
        coming_soon (Union[Unset, bool]): If the artifact is coming soon
        description (Union[Unset, str]): Description of the artifact
        display_name (Union[Unset, str]): Display name of the artifact
        enterprise (Union[Unset, bool]): If the artifact is enterprise
        entrypoint (Union[Unset, MCPDefinitionEntrypoint]): Entrypoint of the artifact
        form (Union[Unset, MCPDefinitionForm]): Form of the artifact
        hidden_secrets (Union[Unset, list[str]]): Hidden secrets of the artifact
        icon (Union[Unset, str]): Icon of the artifact
        image (Union[Unset, str]): Image of the artifact
        integration (Union[Unset, str]): Integration of the artifact
        long_description (Union[Unset, str]): Long description of the artifact
        name (Union[Unset, str]): Name of the artifact
        url (Union[Unset, str]): URL of the artifact
    
    Method generated by attrs for class MCPDefinition.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `categories`
    :

    `coming_soon`
    :

    `created_at`
    :

    `description`
    :

    `display_name`
    :

    `enterprise`
    :

    `entrypoint`
    :

    `form`
    :

    `hidden_secrets`
    :

    `icon`
    :

    `image`
    :

    `integration`
    :

    `long_description`
    :

    `name`
    :

    `updated_at`
    :

    `url`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MCPDefinitionEntrypoint()`
:   Entrypoint of the artifact
    
    Method generated by attrs for class MCPDefinitionEntrypoint.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MCPDefinitionForm()`
:   Form of the artifact
    
    Method generated by attrs for class MCPDefinitionForm.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MemoryAllocationMetric(total_allocation: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Metrics for memory allocation
    
    Attributes:
        total_allocation (Union[Unset, float]): Total memory allocation in GB-seconds
    
    Method generated by attrs for class MemoryAllocationMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `total_allocation: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Metadata(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, labels: blaxel.types.Unset | ForwardRef('MetadataLabels') = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Metadata
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        display_name (Union[Unset, str]): Model display name
        labels (Union[Unset, MetadataLabels]): Labels
        name (Union[Unset, str]): Model name
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class Metadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `created_at`
    :

    `created_by`
    :

    `display_name`
    :

    `labels`
    :

    `name`
    :

    `updated_at`
    :

    `updated_by`
    :

    `workspace`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MetadataLabels()`
:   Labels
    
    Method generated by attrs for class MetadataLabels.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, str]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Metric(rate: blaxel.types.Unset | int = <blaxel.types.Unset object>, request_total: blaxel.types.Unset | int = <blaxel.types.Unset object>, timestamp: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Metric
    
    Attributes:
        rate (Union[Unset, int]): Metric value
        request_total (Union[Unset, int]): Metric value
        timestamp (Union[Unset, str]): Metric timestamp
    
    Method generated by attrs for class Metric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `rate: blaxel.types.Unset | int`
    :

    `request_total: blaxel.types.Unset | int`
    :

    `timestamp: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Metrics(agents: blaxel.types.Unset | Any = <blaxel.types.Unset object>, functions: blaxel.types.Unset | Any = <blaxel.types.Unset object>, inference_global: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, models: blaxel.types.Unset | ForwardRef('MetricsModels') = <blaxel.types.Unset object>, request_total: blaxel.types.Unset | float = <blaxel.types.Unset object>, request_total_per_code: blaxel.types.Unset | ForwardRef('MetricsRequestTotalPerCode') = <blaxel.types.Unset object>, rps: blaxel.types.Unset | float = <blaxel.types.Unset object>, rps_per_code: blaxel.types.Unset | ForwardRef('MetricsRpsPerCode') = <blaxel.types.Unset object>)`
:   Metrics for resources
    
    Attributes:
        agents (Union[Unset, Any]): Metrics for agents
        functions (Union[Unset, Any]): Metrics for functions
        inference_global (Union[Unset, list[Any]]): Historical requests for all resources globally
        models (Union[Unset, MetricsModels]): Metrics for models
        request_total (Union[Unset, float]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, MetricsRequestTotalPerCode]): Number of requests for all resources globally
            per code
        rps (Union[Unset, float]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, MetricsRpsPerCode]): Number of requests per second for all resources globally per
            code
    
    Method generated by attrs for class Metrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `agents`
    :

    `functions`
    :

    `inference_global`
    :

    `models`
    :

    `request_total`
    :

    `request_total_per_code`
    :

    `rps`
    :

    `rps_per_code`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MetricsModels()`
:   Metrics for models
    
    Method generated by attrs for class MetricsModels.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MetricsRequestTotalPerCode()`
:   Number of requests for all resources globally per code
    
    Method generated by attrs for class MetricsRequestTotalPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MetricsRpsPerCode()`
:   Number of requests per second for all resources globally per code
    
    Method generated by attrs for class MetricsRpsPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Model(events: blaxel.types.Unset | list['CoreEvent'] = <blaxel.types.Unset object>, metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('ModelSpec') = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Logical object representing a model
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, ModelSpec]): Model specification
        status (Union[Unset, str]): Model status
    
    Method generated by attrs for class Model.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `events`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ModelPrivateCluster(base_url: blaxel.types.Unset | str = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Private cluster where the model deployment is deployed
    
    Attributes:
        base_url (Union[Unset, str]): The base url of the model in the private cluster
        enabled (Union[Unset, bool]): If true, the private cluster is available
        name (Union[Unset, str]): The name of the private cluster
    
    Method generated by attrs for class ModelPrivateCluster.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `base_url: blaxel.types.Unset | str`
    :

    `enabled: blaxel.types.Unset | bool`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ModelSpec(configurations: blaxel.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.types.Unset object>, enabled: blaxel.types.Unset | bool = <blaxel.types.Unset object>, flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, integration_connections: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, pod_template: blaxel.types.Unset | ForwardRef('PodTemplateSpec') = <blaxel.types.Unset object>, policies: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, private_clusters: blaxel.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.types.Unset object>, revision: blaxel.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.types.Unset object>, runtime: blaxel.types.Unset | ForwardRef('Runtime') = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, serverless_config: blaxel.types.Unset | ForwardRef('ServerlessConfig') = <blaxel.types.Unset object>)`
:   Model specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the agent
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        pod_template (Union[Unset, PodTemplateSpec]): Pod template specification
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        serverless_config (Union[Unset, ServerlessConfig]): Configuration for a serverless deployment
    
    Method generated by attrs for class ModelSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `configurations`
    :

    `enabled`
    :

    `flavors`
    :

    `integration_connections`
    :

    `pod_template`
    :

    `policies`
    :

    `private_clusters`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `serverless_config`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`OAuth(scope: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   OAuth of the artifact
    
    Attributes:
        scope (Union[Unset, list[Any]]): Scope of the OAuth
        type_ (Union[Unset, str]): Type of the OAuth
    
    Method generated by attrs for class OAuth.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `scope: blaxel.types.Unset | list[typing.Any]`
    :

    `type_: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`OwnerFields(created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Owner fields for Persistance
    
    Attributes:
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
    
    Method generated by attrs for class OwnerFields.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_by: blaxel.types.Unset | str`
    :

    `updated_by: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitation(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, email: blaxel.types.Unset | str = <blaxel.types.Unset object>, invited_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, role: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Pending invitation in workspace
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        email (Union[Unset, str]): User email
        invited_by (Union[Unset, str]): User sub
        role (Union[Unset, str]): ACL role
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class PendingInvitation.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `created_by: blaxel.types.Unset | str`
    :

    `email: blaxel.types.Unset | str`
    :

    `invited_by: blaxel.types.Unset | str`
    :

    `role: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    `updated_by: blaxel.types.Unset | str`
    :

    `workspace: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationAccept(email: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | ForwardRef('Workspace') = <blaxel.types.Unset object>)`
:   Pending invitation accept
    
    Attributes:
        email (Union[Unset, str]): User email
        workspace (Union[Unset, Workspace]): Workspace
    
    Method generated by attrs for class PendingInvitationAccept.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `email`
    :

    `workspace`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationRender(email: blaxel.types.Unset | str = <blaxel.types.Unset object>, invited_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, invited_by: blaxel.types.Unset | ForwardRef('PendingInvitationRenderInvitedBy') = <blaxel.types.Unset object>, role: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | ForwardRef('PendingInvitationRenderWorkspace') = <blaxel.types.Unset object>, workspace_details: blaxel.types.Unset | ForwardRef('PendingInvitationWorkspaceDetails') = <blaxel.types.Unset object>)`
:   Pending invitation in workspace
    
    Attributes:
        email (Union[Unset, str]): User email
        invited_at (Union[Unset, str]): Invitation date
        invited_by (Union[Unset, PendingInvitationRenderInvitedBy]): Invited by
        role (Union[Unset, str]): ACL role
        workspace (Union[Unset, PendingInvitationRenderWorkspace]): Workspace
        workspace_details (Union[Unset, PendingInvitationWorkspaceDetails]): Workspace details
    
    Method generated by attrs for class PendingInvitationRender.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `email`
    :

    `invited_at`
    :

    `invited_by`
    :

    `role`
    :

    `workspace`
    :

    `workspace_details`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationRenderInvitedBy(email: blaxel.types.Unset | str = <blaxel.types.Unset object>, family_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, given_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, sub: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Invited by
    
    Attributes:
        email (Union[Unset, str]): User email
        family_name (Union[Unset, str]): User family name
        given_name (Union[Unset, str]): User given name
        sub (Union[Unset, str]): User sub
    
    Method generated by attrs for class PendingInvitationRenderInvitedBy.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `email: blaxel.types.Unset | str`
    :

    `family_name: blaxel.types.Unset | str`
    :

    `given_name: blaxel.types.Unset | str`
    :

    `sub: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationRenderWorkspace(display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Workspace
    
    Attributes:
        display_name (Union[Unset, str]): Workspace display name
        name (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class PendingInvitationRenderWorkspace.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `display_name: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationWorkspaceDetails(emails: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, user_number: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Workspace details
    
    Attributes:
        emails (Union[Unset, list[Any]]): List of user emails in the workspace
        user_number (Union[Unset, float]): Number of users in the workspace
    
    Method generated by attrs for class PendingInvitationWorkspaceDetails.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `emails: blaxel.types.Unset | list[typing.Any]`
    :

    `user_number: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PodTemplateSpec()`
:   Pod template specification
    
    Method generated by attrs for class PodTemplateSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Policy(metadata: blaxel.types.Unset | ForwardRef('Metadata') = <blaxel.types.Unset object>, spec: blaxel.types.Unset | ForwardRef('PolicySpec') = <blaxel.types.Unset object>)`
:   Rule that controls how a deployment is made and served (e.g. location restrictions)
    
    Attributes:
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, PolicySpec]): Policy specification
    
    Method generated by attrs for class Policy.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `metadata`
    :

    `spec`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PolicyLocation(name: blaxel.types.Unset | str = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Policy location
    
    Attributes:
        name (Union[Unset, str]): Policy location name
        type_ (Union[Unset, str]): Policy location type
    
    Method generated by attrs for class PolicyLocation.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: blaxel.types.Unset | str`
    :

    `type_: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PolicyMaxTokens(granularity: blaxel.types.Unset | str = <blaxel.types.Unset object>, input_: blaxel.types.Unset | int = <blaxel.types.Unset object>, output: blaxel.types.Unset | int = <blaxel.types.Unset object>, ratio_input_over_output: blaxel.types.Unset | int = <blaxel.types.Unset object>, step: blaxel.types.Unset | int = <blaxel.types.Unset object>, total: blaxel.types.Unset | int = <blaxel.types.Unset object>)`
:   PolicyMaxTokens is a local type that wraps a slice of PolicyMaxTokens
    
    Attributes:
        granularity (Union[Unset, str]): Granularity
        input_ (Union[Unset, int]): Input
        output (Union[Unset, int]): Output
        ratio_input_over_output (Union[Unset, int]): RatioInputOverOutput
        step (Union[Unset, int]): Step
        total (Union[Unset, int]): Total
    
    Method generated by attrs for class PolicyMaxTokens.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `granularity: blaxel.types.Unset | str`
    :

    `input_: blaxel.types.Unset | int`
    :

    `output: blaxel.types.Unset | int`
    :

    `ratio_input_over_output: blaxel.types.Unset | int`
    :

    `step: blaxel.types.Unset | int`
    :

    `total: blaxel.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PolicySpec(flavors: blaxel.types.Unset | list['Flavor'] = <blaxel.types.Unset object>, locations: blaxel.types.Unset | list['PolicyLocation'] = <blaxel.types.Unset object>, max_tokens: blaxel.types.Unset | ForwardRef('PolicyMaxTokens') = <blaxel.types.Unset object>, resource_types: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, sandbox: blaxel.types.Unset | bool = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Policy specification
    
    Attributes:
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        locations (Union[Unset, list['PolicyLocation']]): PolicyLocations is a local type that wraps a slice of Location
        max_tokens (Union[Unset, PolicyMaxTokens]): PolicyMaxTokens is a local type that wraps a slice of
            PolicyMaxTokens
        resource_types (Union[Unset, list[str]]): PolicyResourceTypes is a local type that wraps a slice of
            PolicyResourceType
        sandbox (Union[Unset, bool]): Sandbox mode
        type_ (Union[Unset, str]): Policy type, can be location or flavor
    
    Method generated by attrs for class PolicySpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `flavors`
    :

    `locations`
    :

    `max_tokens`
    :

    `resource_types`
    :

    `sandbox`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PrivateCluster(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, continent: blaxel.types.Unset | str = <blaxel.types.Unset object>, country: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, healthy: blaxel.types.Unset | bool = <blaxel.types.Unset object>, last_health_check_time: blaxel.types.Unset | str = <blaxel.types.Unset object>, latitude: blaxel.types.Unset | str = <blaxel.types.Unset object>, longitude: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, owned_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   A private cluster where models can be located on.
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        continent (Union[Unset, str]): The private cluster's continent, used to determine the closest private cluster to
            serve inference requests based on the user's location
        country (Union[Unset, str]): The country where the private cluster is located, used to determine the closest
            private cluster to serve inference requests based on the user's location
        display_name (Union[Unset, str]): The private cluster's display Name
        healthy (Union[Unset, bool]): Whether the private cluster is healthy or not, used to determine if the private
            cluster is ready to run inference
        last_health_check_time (Union[Unset, str]): The private cluster's unique name
        latitude (Union[Unset, str]): The private cluster's latitude, used to determine the closest private cluster to
            serve inference requests based on the user's location
        longitude (Union[Unset, str]): The private cluster's longitude, used to determine the closest private cluster to
            serve inference requests based on the user's location
        name (Union[Unset, str]): The name of the private cluster, it must be unique
        owned_by (Union[Unset, str]): The service account (operator) that owns the cluster
        workspace (Union[Unset, str]): The workspace the private cluster belongs to
    
    Method generated by attrs for class PrivateCluster.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `continent: blaxel.types.Unset | str`
    :

    `country: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `created_by: blaxel.types.Unset | str`
    :

    `display_name: blaxel.types.Unset | str`
    :

    `healthy: blaxel.types.Unset | bool`
    :

    `last_health_check_time: blaxel.types.Unset | str`
    :

    `latitude: blaxel.types.Unset | str`
    :

    `longitude: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `owned_by: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    `updated_by: blaxel.types.Unset | str`
    :

    `workspace: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PrivateLocation(name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Private location available for policies
    
    Attributes:
        name (Union[Unset, str]): Location name
    
    Method generated by attrs for class PrivateLocation.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Repository(type_: blaxel.types.Unset | str = <blaxel.types.Unset object>, url: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Repository
    
    Attributes:
        type_ (Union[Unset, str]): Repository type
        url (Union[Unset, str]): Repository URL
    
    Method generated by attrs for class Repository.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `type_: blaxel.types.Unset | str`
    :

    `url: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestDurationOverTimeMetric(average: blaxel.types.Unset | float = <blaxel.types.Unset object>, p50: blaxel.types.Unset | float = <blaxel.types.Unset object>, p90: blaxel.types.Unset | float = <blaxel.types.Unset object>, p99: blaxel.types.Unset | float = <blaxel.types.Unset object>, timestamp: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Request duration over time metric
    
    Attributes:
        average (Union[Unset, float]): Average request duration
        p50 (Union[Unset, float]): P50 request duration
        p90 (Union[Unset, float]): P90 request duration
        p99 (Union[Unset, float]): P99 request duration
        timestamp (Union[Unset, str]): Timestamp
    
    Method generated by attrs for class RequestDurationOverTimeMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `average: blaxel.types.Unset | float`
    :

    `p50: blaxel.types.Unset | float`
    :

    `p90: blaxel.types.Unset | float`
    :

    `p99: blaxel.types.Unset | float`
    :

    `timestamp: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestDurationOverTimeMetrics(request_duration_over_time: blaxel.types.Unset | ForwardRef('RequestDurationOverTimeMetric') = <blaxel.types.Unset object>)`
:   Request duration over time metrics
    
    Attributes:
        request_duration_over_time (Union[Unset, RequestDurationOverTimeMetric]): Request duration over time metric
    
    Method generated by attrs for class RequestDurationOverTimeMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `request_duration_over_time`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalByOriginMetric(request_total_by_origin: blaxel.types.Unset | ForwardRef('RequestTotalByOriginMetricRequestTotalByOrigin') = <blaxel.types.Unset object>, request_total_by_origin_and_code: blaxel.types.Unset | ForwardRef('RequestTotalByOriginMetricRequestTotalByOriginAndCode') = <blaxel.types.Unset object>)`
:   Request total by origin metric
    
    Attributes:
        request_total_by_origin (Union[Unset, RequestTotalByOriginMetricRequestTotalByOrigin]): Request total by origin
        request_total_by_origin_and_code (Union[Unset, RequestTotalByOriginMetricRequestTotalByOriginAndCode]): Request
            total by origin and code
    
    Method generated by attrs for class RequestTotalByOriginMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `request_total_by_origin`
    :

    `request_total_by_origin_and_code`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalByOriginMetricRequestTotalByOrigin()`
:   Request total by origin
    
    Method generated by attrs for class RequestTotalByOriginMetricRequestTotalByOrigin.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalByOriginMetricRequestTotalByOriginAndCode()`
:   Request total by origin and code
    
    Method generated by attrs for class RequestTotalByOriginMetricRequestTotalByOriginAndCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalMetric(request_total: blaxel.types.Unset | float = <blaxel.types.Unset object>, request_total_per_code: blaxel.types.Unset | ForwardRef('RequestTotalMetricRequestTotalPerCode') = <blaxel.types.Unset object>, rps: blaxel.types.Unset | float = <blaxel.types.Unset object>, rps_per_code: blaxel.types.Unset | ForwardRef('RequestTotalMetricRpsPerCode') = <blaxel.types.Unset object>)`
:   Metrics for request total
    
    Attributes:
        request_total (Union[Unset, float]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, RequestTotalMetricRequestTotalPerCode]): Number of requests for all
            resources globally per code
        rps (Union[Unset, float]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, RequestTotalMetricRpsPerCode]): Number of requests for all resources globally
    
    Method generated by attrs for class RequestTotalMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `request_total`
    :

    `request_total_per_code`
    :

    `rps`
    :

    `rps_per_code`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalMetricRequestTotalPerCode()`
:   Number of requests for all resources globally per code
    
    Method generated by attrs for class RequestTotalMetricRequestTotalPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestTotalMetricRpsPerCode()`
:   Number of requests for all resources globally
    
    Method generated by attrs for class RequestTotalMetricRpsPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceLog(message: blaxel.types.Unset | str = <blaxel.types.Unset object>, severity: blaxel.types.Unset | int = <blaxel.types.Unset object>, timestamp: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Log for a resource deployment (eg. model deployment, function deployment)
    
    Attributes:
        message (Union[Unset, str]): Content of the log
        severity (Union[Unset, int]): Severity of the log
        timestamp (Union[Unset, str]): The timestamp of the log
    
    Method generated by attrs for class ResourceLog.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `message: blaxel.types.Unset | str`
    :

    `severity: blaxel.types.Unset | int`
    :

    `timestamp: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceMetrics(inference_global: blaxel.types.Unset | list['Metric'] = <blaxel.types.Unset object>, last_n_requests: blaxel.types.Unset | list['Metric'] = <blaxel.types.Unset object>, latency: blaxel.types.Unset | ForwardRef('LatencyMetric') = <blaxel.types.Unset object>, memory_allocation: blaxel.types.Unset | ForwardRef('MemoryAllocationMetric') = <blaxel.types.Unset object>, model_ttft: blaxel.types.Unset | ForwardRef('LatencyMetric') = <blaxel.types.Unset object>, model_ttft_over_time: blaxel.types.Unset | ForwardRef('TimeToFirstTokenOverTimeMetrics') = <blaxel.types.Unset object>, request_duration_over_time: blaxel.types.Unset | ForwardRef('RequestDurationOverTimeMetrics') = <blaxel.types.Unset object>, request_total: blaxel.types.Unset | float = <blaxel.types.Unset object>, request_total_by_origin: blaxel.types.Unset | ForwardRef('RequestTotalByOriginMetric') = <blaxel.types.Unset object>, request_total_per_code: blaxel.types.Unset | ForwardRef('ResourceMetricsRequestTotalPerCode') = <blaxel.types.Unset object>, rps: blaxel.types.Unset | float = <blaxel.types.Unset object>, rps_per_code: blaxel.types.Unset | ForwardRef('ResourceMetricsRpsPerCode') = <blaxel.types.Unset object>, token_rate: blaxel.types.Unset | ForwardRef('TokenRateMetrics') = <blaxel.types.Unset object>, token_total: blaxel.types.Unset | ForwardRef('TokenTotalMetric') = <blaxel.types.Unset object>)`
:   Metrics for a single resource deployment (eg. model deployment, function deployment)
    
    Attributes:
        inference_global (Union[Unset, list['Metric']]): Array of metrics
        last_n_requests (Union[Unset, list['Metric']]): Array of metrics
        latency (Union[Unset, LatencyMetric]): Latency metrics
        memory_allocation (Union[Unset, MemoryAllocationMetric]): Metrics for memory allocation
        model_ttft (Union[Unset, LatencyMetric]): Latency metrics
        model_ttft_over_time (Union[Unset, TimeToFirstTokenOverTimeMetrics]): Time to first token over time metrics
        request_duration_over_time (Union[Unset, RequestDurationOverTimeMetrics]): Request duration over time metrics
        request_total (Union[Unset, float]): Number of requests for the resource globally
        request_total_by_origin (Union[Unset, RequestTotalByOriginMetric]): Request total by origin metric
        request_total_per_code (Union[Unset, ResourceMetricsRequestTotalPerCode]): Number of requests for the resource
            globally per code
        rps (Union[Unset, float]): Number of requests per second for the resource globally
        rps_per_code (Union[Unset, ResourceMetricsRpsPerCode]): Number of requests per second for the resource globally
            per code
        token_rate (Union[Unset, TokenRateMetrics]): Token rate metrics
        token_total (Union[Unset, TokenTotalMetric]): Token total metric
    
    Method generated by attrs for class ResourceMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `inference_global`
    :

    `last_n_requests`
    :

    `latency`
    :

    `memory_allocation`
    :

    `model_ttft`
    :

    `model_ttft_over_time`
    :

    `request_duration_over_time`
    :

    `request_total`
    :

    `request_total_by_origin`
    :

    `request_total_per_code`
    :

    `rps`
    :

    `rps_per_code`
    :

    `token_rate`
    :

    `token_total`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceMetricsRequestTotalPerCode()`
:   Number of requests for the resource globally per code
    
    Method generated by attrs for class ResourceMetricsRequestTotalPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceMetricsRpsPerCode()`
:   Number of requests per second for the resource globally per code
    
    Method generated by attrs for class ResourceMetricsRpsPerCode.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RevisionConfiguration(active: blaxel.types.Unset | str = <blaxel.types.Unset object>, canary: blaxel.types.Unset | str = <blaxel.types.Unset object>, canary_percent: blaxel.types.Unset | int = <blaxel.types.Unset object>, traffic: blaxel.types.Unset | int = <blaxel.types.Unset object>)`
:   Revision configuration
    
    Attributes:
        active (Union[Unset, str]): Active revision id
        canary (Union[Unset, str]): Canary revision id
        canary_percent (Union[Unset, int]): Canary revision percent
        traffic (Union[Unset, int]): Traffic percentage
    
    Method generated by attrs for class RevisionConfiguration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `active: blaxel.types.Unset | str`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `canary: blaxel.types.Unset | str`
    :

    `canary_percent: blaxel.types.Unset | int`
    :

    `traffic: blaxel.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RevisionMetadata(active: blaxel.types.Unset | bool = <blaxel.types.Unset object>, canary: blaxel.types.Unset | bool = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, id: blaxel.types.Unset | str = <blaxel.types.Unset object>, previous_active: blaxel.types.Unset | bool = <blaxel.types.Unset object>, status: blaxel.types.Unset | str = <blaxel.types.Unset object>, traffic_percent: blaxel.types.Unset | int = <blaxel.types.Unset object>)`
:   Revision metadata
    
    Attributes:
        active (Union[Unset, bool]): Is the revision active
        canary (Union[Unset, bool]): Is the revision canary
        created_at (Union[Unset, str]): Revision created at
        created_by (Union[Unset, str]): Revision created by
        id (Union[Unset, str]): Revision ID
        previous_active (Union[Unset, bool]): Is the revision previous active
        status (Union[Unset, str]): Status of the revision
        traffic_percent (Union[Unset, int]): Percent of traffic to the revision
    
    Method generated by attrs for class RevisionMetadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `active: blaxel.types.Unset | bool`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `canary: blaxel.types.Unset | bool`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `created_by: blaxel.types.Unset | str`
    :

    `id: blaxel.types.Unset | str`
    :

    `previous_active: blaxel.types.Unset | bool`
    :

    `status: blaxel.types.Unset | str`
    :

    `traffic_percent: blaxel.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Runtime(args: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, command: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, cpu: blaxel.types.Unset | int = <blaxel.types.Unset object>, endpoint_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, envs: blaxel.types.Unset | list[typing.Any] = <blaxel.types.Unset object>, image: blaxel.types.Unset | str = <blaxel.types.Unset object>, memory: blaxel.types.Unset | int = <blaxel.types.Unset object>, metric_port: blaxel.types.Unset | int = <blaxel.types.Unset object>, model: blaxel.types.Unset | str = <blaxel.types.Unset object>, organization: blaxel.types.Unset | str = <blaxel.types.Unset object>, serving_port: blaxel.types.Unset | int = <blaxel.types.Unset object>, startup_probe: blaxel.types.Unset | ForwardRef('RuntimeStartupProbe') = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Set of configurations for a deployment
    
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
    
    Method generated by attrs for class Runtime.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `args`
    :

    `command`
    :

    `cpu`
    :

    `endpoint_name`
    :

    `envs`
    :

    `image`
    :

    `memory`
    :

    `metric_port`
    :

    `model`
    :

    `organization`
    :

    `serving_port`
    :

    `startup_probe`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RuntimeStartupProbe()`
:   The readiness probe. Should be a Kubernetes Probe type
    
    Method generated by attrs for class RuntimeStartupProbe.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ServerlessConfig(max_scale: blaxel.types.Unset | int = <blaxel.types.Unset object>, min_scale: blaxel.types.Unset | int = <blaxel.types.Unset object>, timeout: blaxel.types.Unset | int = <blaxel.types.Unset object>)`
:   Configuration for a serverless deployment
    
    Attributes:
        max_scale (Union[Unset, int]): The minimum number of replicas for the deployment. Can be 0 or 1 (in which case
            the deployment is always running in at least one location).
        min_scale (Union[Unset, int]): The maximum number of replicas for the deployment.
        timeout (Union[Unset, int]): The timeout for the deployment in seconds
    
    Method generated by attrs for class ServerlessConfig.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `max_scale: blaxel.types.Unset | int`
    :

    `min_scale: blaxel.types.Unset | int`
    :

    `timeout: blaxel.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SpecConfiguration(secret: blaxel.types.Unset | bool = <blaxel.types.Unset object>, value: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Configuration, this is a key value storage. In your object you can retrieve the value with config[key]
    
    Attributes:
        secret (Union[Unset, bool]): ACconfiguration secret
        value (Union[Unset, str]): Configuration value
    
    Method generated by attrs for class SpecConfiguration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `secret: blaxel.types.Unset | bool`
    :

    `value: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StoreAgent(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, configuration: blaxel.types.Unset | list['StoreConfiguration'] = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, image: blaxel.types.Unset | str = <blaxel.types.Unset object>, labels: blaxel.types.Unset | ForwardRef('StoreAgentLabels') = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, prompt: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Store agent
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        configuration (Union[Unset, list['StoreConfiguration']]): Store agent configuration
        description (Union[Unset, str]): Store agent description
        display_name (Union[Unset, str]): Store agent display name
        image (Union[Unset, str]): Store agent image
        labels (Union[Unset, StoreAgentLabels]): Store agent labels
        name (Union[Unset, str]): Store agent name
        prompt (Union[Unset, str]): Store agent prompt, this is to define what the agent does
    
    Method generated by attrs for class StoreAgent.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `configuration`
    :

    `created_at`
    :

    `created_by`
    :

    `description`
    :

    `display_name`
    :

    `image`
    :

    `labels`
    :

    `name`
    :

    `prompt`
    :

    `updated_at`
    :

    `updated_by`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StoreAgentLabels()`
:   Store agent labels
    
    Method generated by attrs for class StoreAgentLabels.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StoreConfiguration(available_models: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, if_: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, options: blaxel.types.Unset | list['StoreConfigurationOption'] = <blaxel.types.Unset object>, required: blaxel.types.Unset | bool = <blaxel.types.Unset object>, secret: blaxel.types.Unset | bool = <blaxel.types.Unset object>, type_: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Store configuration for resources (eg: agent, function, etc)
    
    Attributes:
        available_models (Union[Unset, list[str]]): Available models for the configuration
        description (Union[Unset, str]): Store configuration description
        display_name (Union[Unset, str]): Store configuration display name
        if_ (Union[Unset, str]): Conditional rendering for the configuration, example: provider === 'openai'
        name (Union[Unset, str]): Store configuration name
        options (Union[Unset, list['StoreConfigurationOption']]):
        required (Union[Unset, bool]): Store configuration required
        secret (Union[Unset, bool]): Store configuration secret
        type_ (Union[Unset, str]): Store configuration type
    
    Method generated by attrs for class StoreConfiguration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `available_models`
    :

    `description`
    :

    `display_name`
    :

    `if_`
    :

    `name`
    :

    `options`
    :

    `required`
    :

    `secret`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StoreConfigurationOption(if_: blaxel.types.Unset | str = <blaxel.types.Unset object>, label: blaxel.types.Unset | str = <blaxel.types.Unset object>, value: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Store configuration options for a select type configuration
    
    Attributes:
        if_ (Union[Unset, str]): Conditional rendering for the configuration option, example: provider === 'openai'
        label (Union[Unset, str]): Store configuration option label
        value (Union[Unset, str]): Store configuration option value
    
    Method generated by attrs for class StoreConfigurationOption.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `if_: blaxel.types.Unset | str`
    :

    `label: blaxel.types.Unset | str`
    :

    `value: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Template(default_branch: blaxel.types.Unset | str = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, download_count: blaxel.types.Unset | int = <blaxel.types.Unset object>, forks_count: blaxel.types.Unset | int = <blaxel.types.Unset object>, icon: blaxel.types.Unset | str = <blaxel.types.Unset object>, icon_dark: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, sha: blaxel.types.Unset | str = <blaxel.types.Unset object>, star_count: blaxel.types.Unset | int = <blaxel.types.Unset object>, topics: blaxel.types.Unset | list[str] = <blaxel.types.Unset object>, url: blaxel.types.Unset | str = <blaxel.types.Unset object>, variables: blaxel.types.Unset | list['TemplateVariable'] = <blaxel.types.Unset object>)`
:   Blaxel template
    
    Attributes:
        default_branch (Union[Unset, str]): Default branch of the template
        description (Union[Unset, str]): Description of the template
        download_count (Union[Unset, int]): Number of downloads/clones of the repository
        forks_count (Union[Unset, int]): Number of forks the repository has
        icon (Union[Unset, str]): URL to the template's icon
        icon_dark (Union[Unset, str]): URL to the template's icon in dark mode
        name (Union[Unset, str]): Name of the template
        sha (Union[Unset, str]): SHA of the variable
        star_count (Union[Unset, int]): Number of stars the repository has
        topics (Union[Unset, list[str]]): Topic of the template
        url (Union[Unset, str]): URL of the template
        variables (Union[Unset, list['TemplateVariable']]): Variables of the template
    
    Method generated by attrs for class Template.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `default_branch`
    :

    `description`
    :

    `download_count`
    :

    `forks_count`
    :

    `icon`
    :

    `icon_dark`
    :

    `name`
    :

    `sha`
    :

    `star_count`
    :

    `topics`
    :

    `url`
    :

    `variables`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TemplateVariable(description: blaxel.types.Unset | str = <blaxel.types.Unset object>, integration: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, path: blaxel.types.Unset | str = <blaxel.types.Unset object>, secret: blaxel.types.Unset | bool = <blaxel.types.Unset object>)`
:   Blaxel template variable
    
    Attributes:
        description (Union[Unset, str]): Description of the variable
        integration (Union[Unset, str]): Integration of the variable
        name (Union[Unset, str]): Name of the variable
        path (Union[Unset, str]): Path of the variable
        secret (Union[Unset, bool]): Whether the variable is secret
    
    Method generated by attrs for class TemplateVariable.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `description: blaxel.types.Unset | str`
    :

    `integration: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `path: blaxel.types.Unset | str`
    :

    `secret: blaxel.types.Unset | bool`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TimeFields(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Time fields for Persistance
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
    
    Method generated by attrs for class TimeFields.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TimeToFirstTokenOverTimeMetrics(time_to_first_token_over_time: blaxel.types.Unset | ForwardRef('RequestDurationOverTimeMetric') = <blaxel.types.Unset object>)`
:   Time to first token over time metrics
    
    Attributes:
        time_to_first_token_over_time (Union[Unset, RequestDurationOverTimeMetric]): Request duration over time metric
    
    Method generated by attrs for class TimeToFirstTokenOverTimeMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `time_to_first_token_over_time`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TokenRateMetric(model: blaxel.types.Unset | str = <blaxel.types.Unset object>, provider: blaxel.types.Unset | str = <blaxel.types.Unset object>, provider_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, timestamp: blaxel.types.Unset | str = <blaxel.types.Unset object>, token_total: blaxel.types.Unset | float = <blaxel.types.Unset object>, trend: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Token rate metric
    
    Attributes:
        model (Union[Unset, str]): Model ID
        provider (Union[Unset, str]): Provider name
        provider_name (Union[Unset, str]): Provider integration name
        timestamp (Union[Unset, str]): Timestamp
        token_total (Union[Unset, float]): Total tokens
        trend (Union[Unset, float]): Trend
    
    Method generated by attrs for class TokenRateMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `model: blaxel.types.Unset | str`
    :

    `provider: blaxel.types.Unset | str`
    :

    `provider_name: blaxel.types.Unset | str`
    :

    `timestamp: blaxel.types.Unset | str`
    :

    `token_total: blaxel.types.Unset | float`
    :

    `trend: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TokenRateMetrics(token_rate: blaxel.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.types.Unset object>, token_rate_input: blaxel.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.types.Unset object>, token_rate_output: blaxel.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.types.Unset object>)`
:   Token rate metrics
    
    Attributes:
        token_rate (Union[Unset, TokenRateMetric]): Token rate metric
        token_rate_input (Union[Unset, TokenRateMetric]): Token rate metric
        token_rate_output (Union[Unset, TokenRateMetric]): Token rate metric
    
    Method generated by attrs for class TokenRateMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `token_rate`
    :

    `token_rate_input`
    :

    `token_rate_output`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TokenTotalMetric(average_token_input_per_request: blaxel.types.Unset | float = <blaxel.types.Unset object>, average_token_output_per_request: blaxel.types.Unset | float = <blaxel.types.Unset object>, average_token_per_request: blaxel.types.Unset | float = <blaxel.types.Unset object>, token_input: blaxel.types.Unset | float = <blaxel.types.Unset object>, token_output: blaxel.types.Unset | float = <blaxel.types.Unset object>, token_total: blaxel.types.Unset | float = <blaxel.types.Unset object>)`
:   Token total metric
    
    Attributes:
        average_token_input_per_request (Union[Unset, float]): Average input token per request
        average_token_output_per_request (Union[Unset, float]): Average output token per request
        average_token_per_request (Union[Unset, float]): Average token per request
        token_input (Union[Unset, float]): Total input tokens
        token_output (Union[Unset, float]): Total output tokens
        token_total (Union[Unset, float]): Total tokens
    
    Method generated by attrs for class TokenTotalMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `average_token_input_per_request: blaxel.types.Unset | float`
    :

    `average_token_output_per_request: blaxel.types.Unset | float`
    :

    `average_token_per_request: blaxel.types.Unset | float`
    :

    `token_input: blaxel.types.Unset | float`
    :

    `token_output: blaxel.types.Unset | float`
    :

    `token_total: blaxel.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TraceIdsResponse()`
:   Trace IDs response
    
    Method generated by attrs for class TraceIdsResponse.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`UpdateWorkspaceServiceAccountBody(description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
    
    Method generated by attrs for class UpdateWorkspaceServiceAccountBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`UpdateWorkspaceServiceAccountResponse200(client_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, description: blaxel.types.Unset | str = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Attributes:
        client_id (Union[Unset, str]): Service account client ID
        created_at (Union[Unset, str]): Creation timestamp
        description (Union[Unset, str]): Service account description
        name (Union[Unset, str]): Service account name
        updated_at (Union[Unset, str]): Last update timestamp
    
    Method generated by attrs for class UpdateWorkspaceServiceAccountResponse200.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `client_id: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `description: blaxel.types.Unset | str`
    :

    `name: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`UpdateWorkspaceUserRoleBody(role: str)`
:   Attributes:
        role (str): The new role to assign to the user
    
    Method generated by attrs for class UpdateWorkspaceUserRoleBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `role: str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WebsocketChannel(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, connection_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, workspace: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   WebSocket connection details
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        connection_id (Union[Unset, str]): Unique connection ID
        workspace (Union[Unset, str]): Workspace the connection belongs to
    
    Method generated by attrs for class WebsocketChannel.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `connection_id: blaxel.types.Unset | str`
    :

    `created_at: blaxel.types.Unset | str`
    :

    `updated_at: blaxel.types.Unset | str`
    :

    `workspace: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Workspace(created_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_at: blaxel.types.Unset | str = <blaxel.types.Unset object>, created_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, updated_by: blaxel.types.Unset | str = <blaxel.types.Unset object>, account_id: blaxel.types.Unset | str = <blaxel.types.Unset object>, display_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, labels: blaxel.types.Unset | ForwardRef('WorkspaceLabels') = <blaxel.types.Unset object>, name: blaxel.types.Unset | str = <blaxel.types.Unset object>, region: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Workspace
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        account_id (Union[Unset, str]): Workspace account id
        display_name (Union[Unset, str]): Workspace display name
        labels (Union[Unset, WorkspaceLabels]): Workspace labels
        name (Union[Unset, str]): Workspace name
        region (Union[Unset, str]): Workspace write region
    
    Method generated by attrs for class Workspace.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `account_id`
    :

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `created_at`
    :

    `created_by`
    :

    `display_name`
    :

    `labels`
    :

    `name`
    :

    `region`
    :

    `updated_at`
    :

    `updated_by`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WorkspaceLabels()`
:   Workspace labels
    
    Method generated by attrs for class WorkspaceLabels.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WorkspaceUser(accepted: blaxel.types.Unset | bool = <blaxel.types.Unset object>, email: blaxel.types.Unset | str = <blaxel.types.Unset object>, email_verified: blaxel.types.Unset | bool = <blaxel.types.Unset object>, family_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, given_name: blaxel.types.Unset | str = <blaxel.types.Unset object>, role: blaxel.types.Unset | str = <blaxel.types.Unset object>, sub: blaxel.types.Unset | str = <blaxel.types.Unset object>)`
:   Workspace user
    
    Attributes:
        accepted (Union[Unset, bool]): Whether the user has accepted the workspace invitation
        email (Union[Unset, str]): Workspace user email
        email_verified (Union[Unset, bool]): Whether the user's email has been verified
        family_name (Union[Unset, str]): Workspace user family name
        given_name (Union[Unset, str]): Workspace user given name
        role (Union[Unset, str]): Workspace user role
        sub (Union[Unset, str]): Workspace user identifier
    
    Method generated by attrs for class WorkspaceUser.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `accepted: blaxel.types.Unset | bool`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `email: blaxel.types.Unset | str`
    :

    `email_verified: blaxel.types.Unset | bool`
    :

    `family_name: blaxel.types.Unset | str`
    :

    `given_name: blaxel.types.Unset | str`
    :

    `role: blaxel.types.Unset | str`
    :

    `sub: blaxel.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :