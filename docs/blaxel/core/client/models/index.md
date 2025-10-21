Module blaxel.core.client.models
================================
Contains all the data models used in inputs/outputs

Sub-modules
-----------
* blaxel.core.client.models.acl
* blaxel.core.client.models.agent
* blaxel.core.client.models.agent_spec
* blaxel.core.client.models.api_key
* blaxel.core.client.models.billable_time_metric
* blaxel.core.client.models.check_workspace_availability_body
* blaxel.core.client.models.configuration
* blaxel.core.client.models.continent
* blaxel.core.client.models.core_event
* blaxel.core.client.models.core_spec
* blaxel.core.client.models.core_spec_configurations
* blaxel.core.client.models.country
* blaxel.core.client.models.create_api_key_for_service_account_body
* blaxel.core.client.models.create_job_execution_request
* blaxel.core.client.models.create_job_execution_request_tasks_item
* blaxel.core.client.models.create_job_execution_response
* blaxel.core.client.models.create_job_execution_response_tasks_item
* blaxel.core.client.models.create_workspace_service_account_body
* blaxel.core.client.models.create_workspace_service_account_response_200
* blaxel.core.client.models.custom_domain
* blaxel.core.client.models.custom_domain_metadata
* blaxel.core.client.models.custom_domain_spec
* blaxel.core.client.models.custom_domain_spec_txt_records
* blaxel.core.client.models.delete_sandbox_preview_token_response_200
* blaxel.core.client.models.delete_workspace_service_account_response_200
* blaxel.core.client.models.entrypoint
* blaxel.core.client.models.entrypoint_env
* blaxel.core.client.models.expiration_policy
* blaxel.core.client.models.flavor
* blaxel.core.client.models.form
* blaxel.core.client.models.form_config
* blaxel.core.client.models.form_oauth
* blaxel.core.client.models.form_secrets
* blaxel.core.client.models.function
* blaxel.core.client.models.function_spec
* blaxel.core.client.models.get_workspace_service_accounts_response_200_item
* blaxel.core.client.models.histogram_bucket
* blaxel.core.client.models.histogram_stats
* blaxel.core.client.models.integration
* blaxel.core.client.models.integration_additional_infos
* blaxel.core.client.models.integration_connection
* blaxel.core.client.models.integration_connection_spec
* blaxel.core.client.models.integration_connection_spec_config
* blaxel.core.client.models.integration_connection_spec_secret
* blaxel.core.client.models.integration_endpoint
* blaxel.core.client.models.integration_endpoint_token
* blaxel.core.client.models.integration_endpoints
* blaxel.core.client.models.integration_headers
* blaxel.core.client.models.integration_model
* blaxel.core.client.models.integration_organization
* blaxel.core.client.models.integration_query_params
* blaxel.core.client.models.integration_repository
* blaxel.core.client.models.invite_workspace_user_body
* blaxel.core.client.models.job
* blaxel.core.client.models.job_execution
* blaxel.core.client.models.job_execution_config
* blaxel.core.client.models.job_execution_metadata
* blaxel.core.client.models.job_execution_spec
* blaxel.core.client.models.job_execution_stats
* blaxel.core.client.models.job_execution_task
* blaxel.core.client.models.job_execution_task_condition
* blaxel.core.client.models.job_execution_task_metadata
* blaxel.core.client.models.job_execution_task_spec
* blaxel.core.client.models.job_metrics
* blaxel.core.client.models.job_metrics_executions_chart
* blaxel.core.client.models.job_metrics_executions_total
* blaxel.core.client.models.job_metrics_tasks_chart
* blaxel.core.client.models.job_metrics_tasks_total
* blaxel.core.client.models.job_spec
* blaxel.core.client.models.jobs_chart_value
* blaxel.core.client.models.jobs_network_chart
* blaxel.core.client.models.jobs_success_failed_chart
* blaxel.core.client.models.jobs_total
* blaxel.core.client.models.last_n_requests_metric
* blaxel.core.client.models.latency_metric
* blaxel.core.client.models.location_response
* blaxel.core.client.models.logs_response
* blaxel.core.client.models.logs_response_data
* blaxel.core.client.models.mcp_definition
* blaxel.core.client.models.mcp_definition_entrypoint
* blaxel.core.client.models.mcp_definition_form
* blaxel.core.client.models.memory_allocation_by_name
* blaxel.core.client.models.memory_allocation_metric
* blaxel.core.client.models.metadata
* blaxel.core.client.models.metadata_labels
* blaxel.core.client.models.metric
* blaxel.core.client.models.metrics
* blaxel.core.client.models.metrics_models
* blaxel.core.client.models.metrics_request_total_per_code
* blaxel.core.client.models.metrics_rps_per_code
* blaxel.core.client.models.model
* blaxel.core.client.models.model_private_cluster
* blaxel.core.client.models.model_spec
* blaxel.core.client.models.o_auth
* blaxel.core.client.models.owner_fields
* blaxel.core.client.models.pending_invitation
* blaxel.core.client.models.pending_invitation_accept
* blaxel.core.client.models.pending_invitation_render
* blaxel.core.client.models.pending_invitation_render_invited_by
* blaxel.core.client.models.pending_invitation_render_workspace
* blaxel.core.client.models.pending_invitation_workspace_details
* blaxel.core.client.models.pod_template_spec
* blaxel.core.client.models.policy
* blaxel.core.client.models.policy_location
* blaxel.core.client.models.policy_max_tokens
* blaxel.core.client.models.policy_spec
* blaxel.core.client.models.port
* blaxel.core.client.models.preview
* blaxel.core.client.models.preview_metadata
* blaxel.core.client.models.preview_spec
* blaxel.core.client.models.preview_spec_request_headers
* blaxel.core.client.models.preview_spec_response_headers
* blaxel.core.client.models.preview_token
* blaxel.core.client.models.preview_token_metadata
* blaxel.core.client.models.preview_token_spec
* blaxel.core.client.models.private_cluster
* blaxel.core.client.models.private_location
* blaxel.core.client.models.public_ip
* blaxel.core.client.models.public_ips
* blaxel.core.client.models.region
* blaxel.core.client.models.repository
* blaxel.core.client.models.request_duration_over_time_metric
* blaxel.core.client.models.request_duration_over_time_metrics
* blaxel.core.client.models.request_total_by_origin_metric
* blaxel.core.client.models.request_total_by_origin_metric_request_total_by_origin
* blaxel.core.client.models.request_total_by_origin_metric_request_total_by_origin_and_code
* blaxel.core.client.models.request_total_metric
* blaxel.core.client.models.request_total_metric_request_total_per_code
* blaxel.core.client.models.request_total_metric_rps_per_code
* blaxel.core.client.models.request_total_response_data
* blaxel.core.client.models.resource
* blaxel.core.client.models.resource_log
* blaxel.core.client.models.resource_log_chart
* blaxel.core.client.models.resource_log_response
* blaxel.core.client.models.resource_metrics
* blaxel.core.client.models.resource_metrics_request_total_per_code
* blaxel.core.client.models.resource_metrics_request_total_per_code_previous
* blaxel.core.client.models.resource_metrics_rps_per_code
* blaxel.core.client.models.resource_metrics_rps_per_code_previous
* blaxel.core.client.models.resource_trace
* blaxel.core.client.models.revision_configuration
* blaxel.core.client.models.revision_metadata
* blaxel.core.client.models.runtime
* blaxel.core.client.models.runtime_configuration
* blaxel.core.client.models.runtime_startup_probe
* blaxel.core.client.models.sandbox
* blaxel.core.client.models.sandbox_definition
* blaxel.core.client.models.sandbox_lifecycle
* blaxel.core.client.models.sandbox_metrics
* blaxel.core.client.models.sandbox_spec
* blaxel.core.client.models.serverless_config
* blaxel.core.client.models.serverless_config_configuration
* blaxel.core.client.models.spec_configuration
* blaxel.core.client.models.start_sandbox
* blaxel.core.client.models.stop_sandbox
* blaxel.core.client.models.store_agent
* blaxel.core.client.models.store_agent_labels
* blaxel.core.client.models.store_configuration
* blaxel.core.client.models.store_configuration_option
* blaxel.core.client.models.template
* blaxel.core.client.models.template_variable
* blaxel.core.client.models.time_fields
* blaxel.core.client.models.time_to_first_token_over_time_metrics
* blaxel.core.client.models.token_rate_metric
* blaxel.core.client.models.token_rate_metrics
* blaxel.core.client.models.token_total_metric
* blaxel.core.client.models.trace_ids_response
* blaxel.core.client.models.trigger
* blaxel.core.client.models.trigger_configuration
* blaxel.core.client.models.trigger_configuration_task
* blaxel.core.client.models.update_workspace_service_account_body
* blaxel.core.client.models.update_workspace_service_account_response_200
* blaxel.core.client.models.update_workspace_user_role_body
* blaxel.core.client.models.volume
* blaxel.core.client.models.volume_attachment
* blaxel.core.client.models.volume_spec
* blaxel.core.client.models.volume_state
* blaxel.core.client.models.websocket_channel
* blaxel.core.client.models.websocket_message
* blaxel.core.client.models.workspace
* blaxel.core.client.models.workspace_labels
* blaxel.core.client.models.workspace_runtime
* blaxel.core.client.models.workspace_user

Classes
-------

`ACL(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, role: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, subject_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, subject_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `resource_id: blaxel.core.client.types.Unset | str`
    :

    `resource_type: blaxel.core.client.types.Unset | str`
    :

    `role: blaxel.core.client.types.Unset | str`
    :

    `subject_id: blaxel.core.client.types.Unset | str`
    :

    `subject_type: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Agent(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('AgentSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`AgentSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, repository: blaxel.core.client.types.Unset | ForwardRef('Repository') = <blaxel.core.client.types.Unset object>, triggers: blaxel.core.client.types.Unset | list['Trigger'] = <blaxel.core.client.types.Unset object>)`
:   Agent specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        description (Union[Unset, str]): Description, small description computed from the prompt
        repository (Union[Unset, Repository]): Repository
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    
    Method generated by attrs for class AgentSpec.

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

    `policies`
    :

    `private_clusters`
    :

    `repository`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `triggers`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ApiKey(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, api_key: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, expires_in: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sub: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sub_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `api_key: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `expires_in: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `sub: blaxel.core.client.types.Unset | str`
    :

    `sub_type: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `updated_by: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`BillableTimeMetric(billable_time: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, total_allocation: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
:   Billable time metric
    
    Attributes:
        billable_time (Union[Unset, float]): Billable time
        total_allocation (Union[Unset, float]): Total memory allocation in GB-seconds
    
    Method generated by attrs for class BillableTimeMetric.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `billable_time: blaxel.core.client.types.Unset | float`
    :

    `total_allocation: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CheckWorkspaceAvailabilityBody(name: str)`
:   Attributes:
        name (str):
    
    Method generated by attrs for class CheckWorkspaceAvailabilityBody.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Configuration(continents: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, countries: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, private_locations: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, regions: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>)`
:   Configuration
    
    Attributes:
        continents (Union[Unset, list[Any]]): Continents
        countries (Union[Unset, list[Any]]): Countries
        private_locations (Union[Unset, list[Any]]): Private locations managed with blaxel operator
        regions (Union[Unset, list[Any]]): Regions
    
    Method generated by attrs for class Configuration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `continents: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `countries: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `private_locations: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `regions: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Continent(display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreEvent(message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, time: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `message: blaxel.core.client.types.Unset | str`
    :

    `revision: blaxel.core.client.types.Unset | str`
    :

    `status: blaxel.core.client.types.Unset | str`
    :

    `time: blaxel.core.client.types.Unset | str`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>)`
:   Core specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
    
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

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CoreSpecConfigurations(key: blaxel.core.client.types.Unset | ForwardRef('SpecConfiguration') = <blaxel.core.client.types.Unset object>)`
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

`Country(display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateApiKeyForServiceAccountBody(expires_in: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `expires_in: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateJobExecutionRequest(execution_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, job_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, tasks: blaxel.core.client.types.Unset | list['CreateJobExecutionRequestTasksItem'] = <blaxel.core.client.types.Unset object>, workspace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Request to create a job execution
    
    Attributes:
        execution_id (Union[Unset, str]): Execution ID (optional, will be generated if not provided)
        id (Union[Unset, str]): Unique message ID
        job_id (Union[Unset, str]): Job ID
        tasks (Union[Unset, list['CreateJobExecutionRequestTasksItem']]): Array of task parameters for parallel
            execution
        workspace_id (Union[Unset, str]): Workspace ID
    
    Method generated by attrs for class CreateJobExecutionRequest.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `execution_id`
    :

    `id`
    :

    `job_id`
    :

    `tasks`
    :

    `workspace_id`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateJobExecutionRequestTasksItem()`
:   Method generated by attrs for class CreateJobExecutionRequestTasksItem.

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

`CreateJobExecutionResponse(execution_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, job_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, tasks: blaxel.core.client.types.Unset | list['CreateJobExecutionResponseTasksItem'] = <blaxel.core.client.types.Unset object>, workspace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Response for creating a job execution
    
    Attributes:
        execution_id (Union[Unset, str]): Execution ID
        id (Union[Unset, str]): Unique message ID
        job_id (Union[Unset, str]): Job ID
        tasks (Union[Unset, list['CreateJobExecutionResponseTasksItem']]): Array of task parameters for parallel
            execution
        workspace_id (Union[Unset, str]): Workspace ID
    
    Method generated by attrs for class CreateJobExecutionResponse.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `execution_id`
    :

    `id`
    :

    `job_id`
    :

    `tasks`
    :

    `workspace_id`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateJobExecutionResponseTasksItem()`
:   Method generated by attrs for class CreateJobExecutionResponseTasksItem.

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

`CreateWorkspaceServiceAccountBody(name: str, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CreateWorkspaceServiceAccountResponse200(client_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, client_secret: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `client_id: blaxel.core.client.types.Unset | str`
    :

    `client_secret: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CustomDomain(metadata: blaxel.core.client.types.Unset | ForwardRef('CustomDomainMetadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('CustomDomainSpec') = <blaxel.core.client.types.Unset object>)`
:   Custom domain for preview deployments
    The custom domain represents a base domain (e.g., example.com) that will be used
    to serve preview deployments. Each preview will be accessible at a subdomain:
    <preview-id>.preview.<base-domain> (e.g., abc123.preview.example.com)
    
        Attributes:
            metadata (Union[Unset, CustomDomainMetadata]): Custom domain metadata
            spec (Union[Unset, CustomDomainSpec]): Custom domain specification
    
    Method generated by attrs for class CustomDomain.

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

`CustomDomainMetadata(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, labels: blaxel.core.client.types.Unset | ForwardRef('MetadataLabels') = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Custom domain metadata
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        display_name (Union[Unset, str]): Display name for the custom domain
        labels (Union[Unset, MetadataLabels]): Labels
        name (Union[Unset, str]): Domain name (e.g., "example.com")
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class CustomDomainMetadata.

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

`CustomDomainSpec(cname_records: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, last_verified_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, txt_records: blaxel.core.client.types.Unset | ForwardRef('CustomDomainSpecTxtRecords') = <blaxel.core.client.types.Unset object>, verification_error: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Custom domain specification
    
    Attributes:
        cname_records (Union[Unset, str]): CNAME target for the domain
        last_verified_at (Union[Unset, str]): Last verification attempt timestamp
        region (Union[Unset, str]): Region that the custom domain is associated with
        status (Union[Unset, str]): Current status of the domain (pending, verified, failed)
        txt_records (Union[Unset, CustomDomainSpecTxtRecords]): Map of TXT record names to values for domain
            verification
        verification_error (Union[Unset, str]): Error message if verification failed
    
    Method generated by attrs for class CustomDomainSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `cname_records`
    :

    `last_verified_at`
    :

    `region`
    :

    `status`
    :

    `txt_records`
    :

    `verification_error`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`CustomDomainSpecTxtRecords()`
:   Map of TXT record names to values for domain verification
    
    Method generated by attrs for class CustomDomainSpecTxtRecords.

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

`DeleteSandboxPreviewTokenResponse200(message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Attributes:
        message (Union[Unset, str]): Success message
    
    Method generated by attrs for class DeleteSandboxPreviewTokenResponse200.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `message: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`DeleteWorkspaceServiceAccountResponse200(client_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `client_id: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Entrypoint(args: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, command: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, env: blaxel.core.client.types.Unset | ForwardRef('EntrypointEnv') = <blaxel.core.client.types.Unset object>, super_gateway_args: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>)`
:   Entrypoint of the artifact
    
    Attributes:
        args (Union[Unset, list[Any]]): Args of the entrypoint
        command (Union[Unset, str]): Command of the entrypoint
        env (Union[Unset, EntrypointEnv]): Env of the entrypoint
        super_gateway_args (Union[Unset, list[Any]]): Super Gateway args of the entrypoint
    
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

    `super_gateway_args`
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

`ExpirationPolicy(action: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, value: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Expiration policy for sandbox lifecycle management
    
    Attributes:
        action (Union[Unset, str]): Action to take when policy is triggered
        type_ (Union[Unset, str]): Type of expiration policy
        value (Union[Unset, str]): Duration value (e.g., '1h', '24h', '7d')
    
    Method generated by attrs for class ExpirationPolicy.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `action: blaxel.core.client.types.Unset | str`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    `value: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Flavor(name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `name: blaxel.core.client.types.Unset | str`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Form(config: blaxel.core.client.types.Unset | ForwardRef('FormConfig') = <blaxel.core.client.types.Unset object>, oauth: blaxel.core.client.types.Unset | ForwardRef('FormOauth') = <blaxel.core.client.types.Unset object>, secrets: blaxel.core.client.types.Unset | ForwardRef('FormSecrets') = <blaxel.core.client.types.Unset object>)`
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

`Function(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('FunctionSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`FunctionSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, transport: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, triggers: blaxel.core.client.types.Unset | list['Trigger'] = <blaxel.core.client.types.Unset object>)`
:   Function specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        description (Union[Unset, str]): Function description, very important for the agent function to work with an LLM
        transport (Union[Unset, str]): Transport compatibility for the MCP, can be "websocket" or "http-stream"
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    
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

    `transport`
    :

    `triggers`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`GetWorkspaceServiceAccountsResponse200Item(client_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `client_id: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`HistogramBucket(count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, end: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, start: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `count: blaxel.core.client.types.Unset | int`
    :

    `end: blaxel.core.client.types.Unset | float`
    :

    `start: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`HistogramStats(average: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p50: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p90: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p99: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `average: blaxel.core.client.types.Unset | float`
    :

    `p50: blaxel.core.client.types.Unset | float`
    :

    `p90: blaxel.core.client.types.Unset | float`
    :

    `p99: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Integration(additional_infos: blaxel.core.client.types.Unset | ForwardRef('IntegrationAdditionalInfos') = <blaxel.core.client.types.Unset object>, endpoints: blaxel.core.client.types.Unset | ForwardRef('IntegrationEndpoints') = <blaxel.core.client.types.Unset object>, headers: blaxel.core.client.types.Unset | ForwardRef('IntegrationHeaders') = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, organizations: blaxel.core.client.types.Unset | list['IntegrationOrganization'] = <blaxel.core.client.types.Unset object>, params: blaxel.core.client.types.Unset | ForwardRef('IntegrationQueryParams') = <blaxel.core.client.types.Unset object>, repositories: blaxel.core.client.types.Unset | list['IntegrationRepository'] = <blaxel.core.client.types.Unset object>)`
:   Integration
    
    Attributes:
        additional_infos (Union[Unset, IntegrationAdditionalInfos]): Integration additional infos
        endpoints (Union[Unset, IntegrationEndpoints]): Integration endpoints
        headers (Union[Unset, IntegrationHeaders]): Integration headers
        name (Union[Unset, str]): Integration name
        organizations (Union[Unset, list['IntegrationOrganization']]): Integration organizations
        params (Union[Unset, IntegrationQueryParams]): Integration query params
        repositories (Union[Unset, list['IntegrationRepository']]): Integration repositories
    
    Method generated by attrs for class Integration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_infos`
    :

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `endpoints`
    :

    `headers`
    :

    `name`
    :

    `organizations`
    :

    `params`
    :

    `repositories`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationAdditionalInfos()`
:   Integration additional infos
    
    Method generated by attrs for class IntegrationAdditionalInfos.

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

`IntegrationConnection(metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('IntegrationConnectionSpec') = <blaxel.core.client.types.Unset object>)`
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

`IntegrationConnectionSpec(config: blaxel.core.client.types.Unset | ForwardRef('IntegrationConnectionSpecConfig') = <blaxel.core.client.types.Unset object>, integration: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, secret: blaxel.core.client.types.Unset | ForwardRef('IntegrationConnectionSpecSecret') = <blaxel.core.client.types.Unset object>)`
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

`IntegrationEndpoint(body: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ignore_models: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, method: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, models: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, stream_key: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, stream_token: blaxel.core.client.types.Unset | ForwardRef('IntegrationEndpointToken') = <blaxel.core.client.types.Unset object>, token: blaxel.core.client.types.Unset | ForwardRef('IntegrationEndpointToken') = <blaxel.core.client.types.Unset object>)`
:   Integration endpoint
    
    Attributes:
        body (Union[Unset, str]): Integration endpoint body
        ignore_models (Union[Unset, list[Any]]): Integration endpoint ignore models
        method (Union[Unset, str]): Integration endpoint method
        models (Union[Unset, list[Any]]): Integration endpoint models
        stream_key (Union[Unset, str]): Integration endpoint stream key
        stream_token (Union[Unset, IntegrationEndpointToken]): Integration endpoint token
        token (Union[Unset, IntegrationEndpointToken]): Integration endpoint token
    
    Method generated by attrs for class IntegrationEndpoint.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `body`
    :

    `ignore_models`
    :

    `method`
    :

    `models`
    :

    `stream_key`
    :

    `stream_token`
    :

    `token`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationEndpointToken(received: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sent: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, total: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Integration endpoint token
    
    Attributes:
        received (Union[Unset, str]): Integration endpoint token received
        sent (Union[Unset, str]): Integration endpoint token sent
        total (Union[Unset, str]): Integration endpoint token total
    
    Method generated by attrs for class IntegrationEndpointToken.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `received: blaxel.core.client.types.Unset | str`
    :

    `sent: blaxel.core.client.types.Unset | str`
    :

    `total: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationEndpoints()`
:   Integration endpoints
    
    Method generated by attrs for class IntegrationEndpoints.

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

`IntegrationHeaders()`
:   Integration headers
    
    Method generated by attrs for class IntegrationHeaders.

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

`IntegrationModel(author: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, downloads: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, endpoint: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, library_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, likes: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, model_private: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, pipeline_tag: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, tags: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, trending_score: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
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

    `author: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `downloads: blaxel.core.client.types.Unset | int`
    :

    `endpoint: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `library_name: blaxel.core.client.types.Unset | str`
    :

    `likes: blaxel.core.client.types.Unset | int`
    :

    `model_private: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `pipeline_tag: blaxel.core.client.types.Unset | str`
    :

    `tags: blaxel.core.client.types.Unset | list[str]`
    :

    `trending_score: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationOrganization(avatar_url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Integration organization
    
    Attributes:
        avatar_url (Union[Unset, str]): Provider organization avatar URL
        display_name (Union[Unset, str]): Provider organization display name
        id (Union[Unset, str]): Provider organization ID
        name (Union[Unset, str]): Provider organization name
    
    Method generated by attrs for class IntegrationOrganization.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `avatar_url: blaxel.core.client.types.Unset | str`
    :

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`IntegrationQueryParams()`
:   Integration query params
    
    Method generated by attrs for class IntegrationQueryParams.

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

`IntegrationRepository(id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, is_bl: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, organization: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `id: blaxel.core.client.types.Unset | str`
    :

    `is_bl: blaxel.core.client.types.Unset | bool`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `organization: blaxel.core.client.types.Unset | str`
    :

    `url: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`InviteWorkspaceUserBody(email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `email: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Job(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('JobSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, JobSpec]): Job specification
        status (Union[Unset, str]): Job status
    
    Method generated by attrs for class Job.

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

`JobExecution(metadata: blaxel.core.client.types.Unset | ForwardRef('JobExecutionMetadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('JobExecutionSpec') = <blaxel.core.client.types.Unset object>, stats: blaxel.core.client.types.Unset | ForwardRef('JobExecutionStats') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, tasks: blaxel.core.client.types.Unset | list['JobExecutionTask'] = <blaxel.core.client.types.Unset object>)`
:   Job execution
    
    Attributes:
        metadata (Union[Unset, JobExecutionMetadata]): Job execution metadata
        spec (Union[Unset, JobExecutionSpec]): Job execution specification
        stats (Union[Unset, JobExecutionStats]): Job execution statistics
        status (Union[Unset, str]): Job execution status
        tasks (Union[Unset, list['JobExecutionTask']]): List of execution tasks
    
    Method generated by attrs for class JobExecution.

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

    `stats`
    :

    `status`
    :

    `tasks`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionConfig(max_concurrent_tasks: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, max_retries: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timeout: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Configuration for a job execution
    
    Attributes:
        max_concurrent_tasks (Union[Unset, int]): The maximum number of concurrent tasks for an execution
        max_retries (Union[Unset, int]): The maximum number of retries for the job execution
        timeout (Union[Unset, int]): The timeout for the job execution in seconds
    
    Method generated by attrs for class JobExecutionConfig.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `max_concurrent_tasks: blaxel.core.client.types.Unset | int`
    :

    `max_retries: blaxel.core.client.types.Unset | int`
    :

    `timeout: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionMetadata(cluster: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, completed_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, deleted_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, expired_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, job: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, started_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job execution metadata
    
    Attributes:
        cluster (Union[Unset, str]): Cluster ID
        completed_at (Union[Unset, str]): Completion timestamp
        created_at (Union[Unset, str]): Creation timestamp
        deleted_at (Union[Unset, str]): Deletion timestamp
        expired_at (Union[Unset, str]): Expiration timestamp
        id (Union[Unset, str]): Execution ID
        job (Union[Unset, str]): Job name
        started_at (Union[Unset, str]): Start timestamp
        updated_at (Union[Unset, str]): Last update timestamp
        workspace (Union[Unset, str]): Workspace ID
    
    Method generated by attrs for class JobExecutionMetadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `cluster: blaxel.core.client.types.Unset | str`
    :

    `completed_at: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `deleted_at: blaxel.core.client.types.Unset | str`
    :

    `expired_at: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `job: blaxel.core.client.types.Unset | str`
    :

    `started_at: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionSpec(parallelism: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, tasks: blaxel.core.client.types.Unset | list['JobExecutionTask'] = <blaxel.core.client.types.Unset object>)`
:   Job execution specification
    
    Attributes:
        parallelism (Union[Unset, int]): Number of parallel tasks
        tasks (Union[Unset, list['JobExecutionTask']]): List of execution tasks
    
    Method generated by attrs for class JobExecutionSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `parallelism`
    :

    `tasks`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionStats(cancelled: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, failure: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, retried: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, running: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, success: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, total: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Job execution statistics
    
    Attributes:
        cancelled (Union[Unset, int]): Number of cancelled tasks
        failure (Union[Unset, int]): Number of failed tasks
        retried (Union[Unset, int]): Number of retried tasks
        running (Union[Unset, int]): Number of running tasks
        success (Union[Unset, int]): Number of successful tasks
        total (Union[Unset, int]): Total number of tasks
    
    Method generated by attrs for class JobExecutionStats.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `cancelled: blaxel.core.client.types.Unset | int`
    :

    `failure: blaxel.core.client.types.Unset | int`
    :

    `retried: blaxel.core.client.types.Unset | int`
    :

    `running: blaxel.core.client.types.Unset | int`
    :

    `success: blaxel.core.client.types.Unset | int`
    :

    `total: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionTask(conditions: blaxel.core.client.types.Unset | list['JobExecutionTaskCondition'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('JobExecutionTaskMetadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('JobExecutionTaskSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job execution task
    
    Attributes:
        conditions (Union[Unset, list['JobExecutionTaskCondition']]): Task conditions
        metadata (Union[Unset, JobExecutionTaskMetadata]): Job execution task metadata
        spec (Union[Unset, JobExecutionTaskSpec]): Job execution task specification
        status (Union[Unset, str]): Job execution task status
    
    Method generated by attrs for class JobExecutionTask.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `conditions`
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

`JobExecutionTaskCondition(execution_reason: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, reason: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, severity: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, state: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job execution task condition
    
    Attributes:
        execution_reason (Union[Unset, str]): Execution reason
        message (Union[Unset, str]): Condition message
        reason (Union[Unset, str]): Condition reason
        severity (Union[Unset, str]): Condition severity
        state (Union[Unset, str]): Condition state
        type_ (Union[Unset, str]): Condition type
    
    Method generated by attrs for class JobExecutionTaskCondition.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `execution_reason: blaxel.core.client.types.Unset | str`
    :

    `message: blaxel.core.client.types.Unset | str`
    :

    `reason: blaxel.core.client.types.Unset | str`
    :

    `severity: blaxel.core.client.types.Unset | str`
    :

    `state: blaxel.core.client.types.Unset | str`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionTaskMetadata(completed_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, scheduled_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, started_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job execution task metadata
    
    Attributes:
        completed_at (Union[Unset, str]): Completion timestamp
        created_at (Union[Unset, str]): Creation timestamp
        name (Union[Unset, str]): Task name
        scheduled_at (Union[Unset, str]): Scheduled timestamp
        started_at (Union[Unset, str]): Start timestamp
        updated_at (Union[Unset, str]): Last update timestamp
    
    Method generated by attrs for class JobExecutionTaskMetadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `completed_at: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `scheduled_at: blaxel.core.client.types.Unset | str`
    :

    `started_at: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobExecutionTaskSpec(max_retries: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timeout: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Job execution task specification
    
    Attributes:
        max_retries (Union[Unset, int]): Maximum number of retries
        timeout (Union[Unset, str]): Task timeout duration
    
    Method generated by attrs for class JobExecutionTaskSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `max_retries: blaxel.core.client.types.Unset | int`
    :

    `timeout: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobMetrics(billable_time: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, cpu_usage: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, executions_chart: blaxel.core.client.types.Unset | ForwardRef('JobMetricsExecutionsChart') = <blaxel.core.client.types.Unset object>, executions_running: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, executions_total: blaxel.core.client.types.Unset | ForwardRef('JobMetricsExecutionsTotal') = <blaxel.core.client.types.Unset object>, ram_usage: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, tasks_chart: blaxel.core.client.types.Unset | ForwardRef('JobMetricsTasksChart') = <blaxel.core.client.types.Unset object>, tasks_running: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, tasks_total: blaxel.core.client.types.Unset | ForwardRef('JobMetricsTasksTotal') = <blaxel.core.client.types.Unset object>)`
:   Metrics for job
    
    Attributes:
        billable_time (Union[Unset, list[Any]]): Billable time
        cpu_usage (Union[Unset, list[Any]]): CPU usage
        executions_chart (Union[Unset, JobMetricsExecutionsChart]): Executions chart
        executions_running (Union[Unset, list[Any]]): Executions running
        executions_total (Union[Unset, JobMetricsExecutionsTotal]): Total executions
        ram_usage (Union[Unset, list[Any]]): RAM usage
        tasks_chart (Union[Unset, JobMetricsTasksChart]): Tasks chart
        tasks_running (Union[Unset, list[Any]]): Tasks running
        tasks_total (Union[Unset, JobMetricsTasksTotal]): Total tasks
    
    Method generated by attrs for class JobMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `billable_time`
    :

    `cpu_usage`
    :

    `executions_chart`
    :

    `executions_running`
    :

    `executions_total`
    :

    `ram_usage`
    :

    `tasks_chart`
    :

    `tasks_running`
    :

    `tasks_total`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobMetricsExecutionsChart()`
:   Executions chart
    
    Method generated by attrs for class JobMetricsExecutionsChart.

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

`JobMetricsExecutionsTotal()`
:   Total executions
    
    Method generated by attrs for class JobMetricsExecutionsTotal.

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

`JobMetricsTasksChart()`
:   Tasks chart
    
    Method generated by attrs for class JobMetricsTasksChart.

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

`JobMetricsTasksTotal()`
:   Total tasks
    
    Method generated by attrs for class JobMetricsTasksTotal.

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

`JobSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, triggers: blaxel.core.client.types.Unset | list['Trigger'] = <blaxel.core.client.types.Unset object>)`
:   Job specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        region (Union[Unset, str]): Region where the job should be created (e.g. us-pdx-1, eu-lon-1)
        triggers (Union[Unset, list['Trigger']]): Triggers to use your agent
    
    Method generated by attrs for class JobSpec.

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

    `policies`
    :

    `private_clusters`
    :

    `region`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `triggers`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobsChartValue(timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, value: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
:   Jobs CPU usage
    
    Attributes:
        timestamp (Union[Unset, str]): Metric timestamp
        value (Union[Unset, float]): Metric value
    
    Method generated by attrs for class JobsChartValue.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `value: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobsNetworkChart(received: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>, sent: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>)`
:   Jobs chart
    
    Attributes:
        received (Union[Unset, JobsChartValue]): Jobs CPU usage
        sent (Union[Unset, JobsChartValue]): Jobs CPU usage
    
    Method generated by attrs for class JobsNetworkChart.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `received`
    :

    `sent`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobsSuccessFailedChart(failed: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>, retried: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>, success: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, total: blaxel.core.client.types.Unset | ForwardRef('JobsChartValue') = <blaxel.core.client.types.Unset object>)`
:   Jobs chart
    
    Attributes:
        failed (Union[Unset, JobsChartValue]): Jobs CPU usage
        retried (Union[Unset, JobsChartValue]): Jobs CPU usage
        success (Union[Unset, JobsChartValue]): Jobs CPU usage
        timestamp (Union[Unset, str]): Metric timestamp
        total (Union[Unset, JobsChartValue]): Jobs CPU usage
    
    Method generated by attrs for class JobsSuccessFailedChart.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `failed`
    :

    `retried`
    :

    `success`
    :

    `timestamp`
    :

    `total`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`JobsTotal(failed: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, retried: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, running: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, success: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, total: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Jobs executions
    
    Attributes:
        failed (Union[Unset, int]): Failed executions
        retried (Union[Unset, int]): Retried executions
        running (Union[Unset, int]): Running executions
        success (Union[Unset, int]): Success executions
        total (Union[Unset, int]): Total executions
    
    Method generated by attrs for class JobsTotal.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `failed: blaxel.core.client.types.Unset | int`
    :

    `retried: blaxel.core.client.types.Unset | int`
    :

    `running: blaxel.core.client.types.Unset | int`
    :

    `success: blaxel.core.client.types.Unset | int`
    :

    `total: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LastNRequestsMetric(date: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, status_code: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workload_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workload_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Last N requests
    
    Attributes:
        date (Union[Unset, str]): Timestamp
        status_code (Union[Unset, str]): Status code
        workload_id (Union[Unset, str]): Workload ID
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

    `date: blaxel.core.client.types.Unset | str`
    :

    `status_code: blaxel.core.client.types.Unset | str`
    :

    `workload_id: blaxel.core.client.types.Unset | str`
    :

    `workload_type: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LatencyMetric(global_histogram: blaxel.core.client.types.Unset | ForwardRef('HistogramBucket') = <blaxel.core.client.types.Unset object>, global_stats: blaxel.core.client.types.Unset | ForwardRef('HistogramStats') = <blaxel.core.client.types.Unset object>, histogram_per_code: blaxel.core.client.types.Unset | ForwardRef('HistogramBucket') = <blaxel.core.client.types.Unset object>, stats_per_code: blaxel.core.client.types.Unset | ForwardRef('HistogramStats') = <blaxel.core.client.types.Unset object>)`
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

`LocationResponse(continent: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, country: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, location: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Location availability for policies
    
    Attributes:
        continent (Union[Unset, str]): Continent of the location
        country (Union[Unset, str]): Country of the location
        flavors (Union[Unset, list['Flavor']]): Hardware flavors available in the location
        location (Union[Unset, str]): Name of the location
        region (Union[Unset, str]): Region of the location
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

    `region`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LogsResponse(data: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>)`
:   Response for logs
    
    Attributes:
        data (Union[Unset, list[Any]]): Data
    
    Method generated by attrs for class LogsResponse.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `data: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`LogsResponseData(body: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, log_attributes: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, severity_number: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, trace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Response data for logs
    
    Attributes:
        body (Union[Unset, str]): Body of the log
        log_attributes (Union[Unset, list[Any]]): Log attributes
        severity_number (Union[Unset, int]): Severity number of the log
        timestamp (Union[Unset, str]): Timestamp of the log
        trace_id (Union[Unset, str]): Trace ID of the log
    
    Method generated by attrs for class LogsResponseData.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `body: blaxel.core.client.types.Unset | str`
    :

    `log_attributes: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `severity_number: blaxel.core.client.types.Unset | int`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `trace_id: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MCPDefinition(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, categories: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, coming_soon: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, enterprise: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, entrypoint: blaxel.core.client.types.Unset | ForwardRef('MCPDefinitionEntrypoint') = <blaxel.core.client.types.Unset object>, form: blaxel.core.client.types.Unset | ForwardRef('MCPDefinitionForm') = <blaxel.core.client.types.Unset object>, hidden_secrets: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, icon: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, image: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, integration: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, long_description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, transport: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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
        transport (Union[Unset, str]): Transport compatibility for the MCP, can be "websocket" or "http-stream"
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

    `transport`
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

`MemoryAllocationByName(allocation: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Memory allocation by service name
    
    Attributes:
        allocation (Union[Unset, float]): Memory allocation value
        name (Union[Unset, str]): Name
    
    Method generated by attrs for class MemoryAllocationByName.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `allocation: blaxel.core.client.types.Unset | float`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`MemoryAllocationMetric(total_allocation: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `total_allocation: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Metadata(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, labels: blaxel.core.client.types.Unset | ForwardRef('MetadataLabels') = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, plan: blaxel.core.client.types.Unset | Any = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Metadata
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        display_name (Union[Unset, str]): Model display name
        labels (Union[Unset, MetadataLabels]): Labels
        name (Union[Unset, str]): Model name
        plan (Union[Unset, Any]): Plan
        url (Union[Unset, str]): URL
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

    `plan`
    :

    `updated_at`
    :

    `updated_by`
    :

    `url`
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

`Metric(rate: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, request_total: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `rate: blaxel.core.client.types.Unset | int`
    :

    `request_total: blaxel.core.client.types.Unset | int`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Metrics(agents: blaxel.core.client.types.Unset | Any = <blaxel.core.client.types.Unset object>, functions: blaxel.core.client.types.Unset | Any = <blaxel.core.client.types.Unset object>, inference_global: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, items: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, last_n_requests: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, models: blaxel.core.client.types.Unset | ForwardRef('MetricsModels') = <blaxel.core.client.types.Unset object>, request_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, request_total_per_code: blaxel.core.client.types.Unset | ForwardRef('MetricsRequestTotalPerCode') = <blaxel.core.client.types.Unset object>, rps: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps_per_code: blaxel.core.client.types.Unset | ForwardRef('MetricsRpsPerCode') = <blaxel.core.client.types.Unset object>, sandboxes: blaxel.core.client.types.Unset | Any = <blaxel.core.client.types.Unset object>)`
:   Metrics for resources
    
    Attributes:
        agents (Union[Unset, Any]): Metrics for agents
        functions (Union[Unset, Any]): Metrics for functions
        inference_global (Union[Unset, list[Any]]): Historical requests for all resources globally
        items (Union[Unset, list[Any]]): Historical requests for all resources globally
        last_n_requests (Union[Unset, int]): Metric value
        models (Union[Unset, MetricsModels]): Metrics for models
        request_total (Union[Unset, float]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, MetricsRequestTotalPerCode]): Number of requests for all resources globally
            per code
        rps (Union[Unset, float]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, MetricsRpsPerCode]): Number of requests per second for all resources globally per
            code
        sandboxes (Union[Unset, Any]): Metrics for sandboxes
    
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

    `items`
    :

    `last_n_requests`
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

    `sandboxes`
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

`Model(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('ModelSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`ModelPrivateCluster(base_url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `base_url: blaxel.core.client.types.Unset | str`
    :

    `enabled: blaxel.core.client.types.Unset | bool`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ModelSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>)`
:   Model specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
    
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

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`OAuth(scope: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `scope: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`OwnerFields(created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `updated_by: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitation(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, invited_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, role: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `email: blaxel.core.client.types.Unset | str`
    :

    `invited_by: blaxel.core.client.types.Unset | str`
    :

    `role: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `updated_by: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationAccept(email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | ForwardRef('Workspace') = <blaxel.core.client.types.Unset object>)`
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

`PendingInvitationRender(email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, invited_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, invited_by: blaxel.core.client.types.Unset | ForwardRef('PendingInvitationRenderInvitedBy') = <blaxel.core.client.types.Unset object>, role: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | ForwardRef('PendingInvitationRenderWorkspace') = <blaxel.core.client.types.Unset object>, workspace_details: blaxel.core.client.types.Unset | ForwardRef('PendingInvitationWorkspaceDetails') = <blaxel.core.client.types.Unset object>)`
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

`PendingInvitationRenderInvitedBy(email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, family_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, given_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sub: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `email: blaxel.core.client.types.Unset | str`
    :

    `family_name: blaxel.core.client.types.Unset | str`
    :

    `given_name: blaxel.core.client.types.Unset | str`
    :

    `sub: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationRenderWorkspace(display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PendingInvitationWorkspaceDetails(emails: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, user_number: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `emails: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `user_number: blaxel.core.client.types.Unset | float`
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

`Policy(metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('PolicySpec') = <blaxel.core.client.types.Unset object>)`
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

`PolicyLocation(name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `name: blaxel.core.client.types.Unset | str`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PolicyMaxTokens(granularity: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, input_: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, output: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, ratio_input_over_output: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, step: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, total: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
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

    `granularity: blaxel.core.client.types.Unset | str`
    :

    `input_: blaxel.core.client.types.Unset | int`
    :

    `output: blaxel.core.client.types.Unset | int`
    :

    `ratio_input_over_output: blaxel.core.client.types.Unset | int`
    :

    `step: blaxel.core.client.types.Unset | int`
    :

    `total: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PolicySpec(flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, locations: blaxel.core.client.types.Unset | list['PolicyLocation'] = <blaxel.core.client.types.Unset object>, max_tokens: blaxel.core.client.types.Unset | ForwardRef('PolicyMaxTokens') = <blaxel.core.client.types.Unset object>, resource_types: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`Port(name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, protocol: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, target: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   A port for a resource
    
    Attributes:
        name (Union[Unset, str]): The name of the port
        protocol (Union[Unset, str]): The protocol of the port
        target (Union[Unset, int]): The target port of the port
    
    Method generated by attrs for class Port.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `protocol: blaxel.core.client.types.Unset | str`
    :

    `target: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Preview(metadata: blaxel.core.client.types.Unset | ForwardRef('PreviewMetadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('PreviewSpec') = <blaxel.core.client.types.Unset object>)`
:   Preview of a Resource
    
    Attributes:
        metadata (Union[Unset, PreviewMetadata]): PreviewMetadata
        spec (Union[Unset, PreviewSpec]): Preview of a Resource
    
    Method generated by attrs for class Preview.

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

`PreviewMetadata(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   PreviewMetadata
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        display_name (Union[Unset, str]): Model display name
        name (Union[Unset, str]): Preview name
        resource_name (Union[Unset, str]): Resource name
        resource_type (Union[Unset, str]): Resource type
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class PreviewMetadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `resource_name: blaxel.core.client.types.Unset | str`
    :

    `resource_type: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `updated_by: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PreviewSpec(custom_domain: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, expires: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, port: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, prefix_url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, public: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, request_headers: blaxel.core.client.types.Unset | ForwardRef('PreviewSpecRequestHeaders') = <blaxel.core.client.types.Unset object>, response_headers: blaxel.core.client.types.Unset | ForwardRef('PreviewSpecResponseHeaders') = <blaxel.core.client.types.Unset object>, ttl: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Preview of a Resource
    
    Attributes:
        custom_domain (Union[Unset, str]): Custom domain bound to this preview
        expires (Union[Unset, str]): The expiration date for the preview in ISO 8601 format - 2024-12-31T23:59:59Z
        port (Union[Unset, int]): Port of the preview
        prefix_url (Union[Unset, str]): Prefix URL
        public (Union[Unset, bool]): Whether the preview is public
        region (Union[Unset, str]): Region where the preview is deployed, this is readonly
        request_headers (Union[Unset, PreviewSpecRequestHeaders]): Those headers will be set in all requests to your
            preview. This is especially useful to set the Authorization header.
        response_headers (Union[Unset, PreviewSpecResponseHeaders]): Those headers will be set in all responses of your
            preview. This is especially useful to set the CORS headers.
        ttl (Union[Unset, str]): Time to live for the preview (e.g., "1h", "24h", "7d"). After this duration, the
            preview will be automatically deleted.
        url (Union[Unset, str]): URL of the preview
    
    Method generated by attrs for class PreviewSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `custom_domain`
    :

    `expires`
    :

    `port`
    :

    `prefix_url`
    :

    `public`
    :

    `region`
    :

    `request_headers`
    :

    `response_headers`
    :

    `ttl`
    :

    `url`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PreviewSpecRequestHeaders()`
:   Those headers will be set in all requests to your preview. This is especially useful to set the Authorization
    header.
    
    Method generated by attrs for class PreviewSpecRequestHeaders.

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

`PreviewSpecResponseHeaders()`
:   Those headers will be set in all responses of your preview. This is especially useful to set the CORS headers.
    
    Method generated by attrs for class PreviewSpecResponseHeaders.

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

`PreviewToken(metadata: blaxel.core.client.types.Unset | ForwardRef('PreviewTokenMetadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('PreviewTokenSpec') = <blaxel.core.client.types.Unset object>)`
:   Token for a Preview
    
    Attributes:
        metadata (Union[Unset, PreviewTokenMetadata]): PreviewTokenMetadata
        spec (Union[Unset, PreviewTokenSpec]): Spec for a Preview Token
    
    Method generated by attrs for class PreviewToken.

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

`PreviewTokenMetadata(name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, preview_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, resource_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   PreviewTokenMetadata
    
    Attributes:
        name (Union[Unset, str]): Token name
        preview_name (Union[Unset, str]): Preview name
        resource_name (Union[Unset, str]): Resource name
        resource_type (Union[Unset, str]): Resource type
        workspace (Union[Unset, str]): Workspace name
    
    Method generated by attrs for class PreviewTokenMetadata.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `preview_name: blaxel.core.client.types.Unset | str`
    :

    `resource_name: blaxel.core.client.types.Unset | str`
    :

    `resource_type: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PreviewTokenSpec(expired: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, expires_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, token: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Spec for a Preview Token
    
    Attributes:
        expired (Union[Unset, bool]): Whether the token is expired
        expires_at (Union[Unset, str]): Expiration time of the token
        token (Union[Unset, str]): Token
    
    Method generated by attrs for class PreviewTokenSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `expired: blaxel.core.client.types.Unset | bool`
    :

    `expires_at: blaxel.core.client.types.Unset | str`
    :

    `token: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PrivateCluster(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, continent: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, country: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, healthy: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, last_health_check_time: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, latitude: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, longitude: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, owned_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `continent: blaxel.core.client.types.Unset | str`
    :

    `country: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `display_name: blaxel.core.client.types.Unset | str`
    :

    `healthy: blaxel.core.client.types.Unset | bool`
    :

    `last_health_check_time: blaxel.core.client.types.Unset | str`
    :

    `latitude: blaxel.core.client.types.Unset | str`
    :

    `longitude: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `owned_by: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `updated_by: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PrivateLocation(name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PublicIp(description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ipv_4_cidrs: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, ipv_6_cidrs: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>)`
:   Attributes:
        description (Union[Unset, str]): Description of the region/location
        ipv_4_cidrs (Union[Unset, list[str]]): List of public ipv4 addresses
        ipv_6_cidrs (Union[Unset, list[str]]): List of public ipv6 addresses
    
    Method generated by attrs for class PublicIp.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `description: blaxel.core.client.types.Unset | str`
    :

    `ipv_4_cidrs: blaxel.core.client.types.Unset | list[str]`
    :

    `ipv_6_cidrs: blaxel.core.client.types.Unset | list[str]`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`PublicIps()`
:   Method generated by attrs for class PublicIps.

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

`Region(allowed: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, continent: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, country: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, info_generation: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, location: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Region
    
    Attributes:
        allowed (Union[Unset, str]): Region display name
        continent (Union[Unset, str]): Region display name
        country (Union[Unset, str]): Region display name
        info_generation (Union[Unset, str]): Region display name
        location (Union[Unset, str]): Region display name
        name (Union[Unset, str]): Region name
    
    Method generated by attrs for class Region.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `allowed: blaxel.core.client.types.Unset | str`
    :

    `continent: blaxel.core.client.types.Unset | str`
    :

    `country: blaxel.core.client.types.Unset | str`
    :

    `info_generation: blaxel.core.client.types.Unset | str`
    :

    `location: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Repository(type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `type_: blaxel.core.client.types.Unset | str`
    :

    `url: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestDurationOverTimeMetric(average: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p50: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p90: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, p99: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `average: blaxel.core.client.types.Unset | float`
    :

    `p50: blaxel.core.client.types.Unset | float`
    :

    `p90: blaxel.core.client.types.Unset | float`
    :

    `p99: blaxel.core.client.types.Unset | float`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RequestDurationOverTimeMetrics(request_duration_over_time: blaxel.core.client.types.Unset | ForwardRef('RequestDurationOverTimeMetric') = <blaxel.core.client.types.Unset object>)`
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

`RequestTotalByOriginMetric(request_total_by_origin: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetricRequestTotalByOrigin') = <blaxel.core.client.types.Unset object>, request_total_by_origin_and_code: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetricRequestTotalByOriginAndCode') = <blaxel.core.client.types.Unset object>)`
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

`RequestTotalMetric(items: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, request_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, request_total_per_code: blaxel.core.client.types.Unset | ForwardRef('RequestTotalMetricRequestTotalPerCode') = <blaxel.core.client.types.Unset object>, rps: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps_per_code: blaxel.core.client.types.Unset | ForwardRef('RequestTotalMetricRpsPerCode') = <blaxel.core.client.types.Unset object>)`
:   Metrics for request total
    
    Attributes:
        items (Union[Unset, list[Any]]): Historical requests for all resources globally
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

    `items`
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

`RequestTotalResponseData(request_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, status_code: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workload_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workload_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Request total response data
    
    Attributes:
        request_total (Union[Unset, float]): Request total
        status_code (Union[Unset, str]): Status code
        workload_id (Union[Unset, str]): Workload ID
        workload_type (Union[Unset, str]): Workload type
        workspace (Union[Unset, str]): Workspace
    
    Method generated by attrs for class RequestTotalResponseData.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `request_total: blaxel.core.client.types.Unset | float`
    :

    `status_code: blaxel.core.client.types.Unset | str`
    :

    `workload_id: blaxel.core.client.types.Unset | str`
    :

    `workload_type: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Resource(infrastructure_generation: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Resource
    
    Attributes:
        infrastructure_generation (Union[Unset, str]): Region of the resource
        name (Union[Unset, str]): Name of the resource
        type_ (Union[Unset, str]): Type of the resource
        workspace (Union[Unset, str]): Workspace of the resource
        workspace_id (Union[Unset, str]): Workspace ID of the resource
    
    Method generated by attrs for class Resource.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `infrastructure_generation: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `type_: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    `workspace_id: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceLog(message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, severity: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, trace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Log for a resource deployment (eg. model deployment, function deployment)
    
    Attributes:
        message (Union[Unset, str]): Content of the log
        severity (Union[Unset, int]): Severity of the log
        timestamp (Union[Unset, str]): The timestamp of the log
        trace_id (Union[Unset, str]): Trace ID of the log
    
    Method generated by attrs for class ResourceLog.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `message: blaxel.core.client.types.Unset | str`
    :

    `severity: blaxel.core.client.types.Unset | int`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `trace_id: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceLogChart(count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, debug: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, error: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, fatal: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, info: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, trace: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, unknown: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, warning: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Chart for a resource log
    
    Attributes:
        count (Union[Unset, int]): Count of the log
        debug (Union[Unset, int]): Debug count of the log
        error (Union[Unset, int]): Error count of the log
        fatal (Union[Unset, int]): Fatal count of the log
        info (Union[Unset, int]): Info count of the log
        timestamp (Union[Unset, str]): Timestamp of the log
        trace (Union[Unset, int]): Trace count of the log
        unknown (Union[Unset, int]): Unknown count of the log
        warning (Union[Unset, int]): Warning count of the log
    
    Method generated by attrs for class ResourceLogChart.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `count: blaxel.core.client.types.Unset | int`
    :

    `debug: blaxel.core.client.types.Unset | int`
    :

    `error: blaxel.core.client.types.Unset | int`
    :

    `fatal: blaxel.core.client.types.Unset | int`
    :

    `info: blaxel.core.client.types.Unset | int`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `trace: blaxel.core.client.types.Unset | int`
    :

    `unknown: blaxel.core.client.types.Unset | int`
    :

    `warning: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceLogResponse(chart: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, logs: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, total_count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Response for a resource log
    
    Attributes:
        chart (Union[Unset, list[Any]]): Chart
        logs (Union[Unset, list[Any]]): Logs
        total_count (Union[Unset, int]): Total count of logs
    
    Method generated by attrs for class ResourceLogResponse.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `chart: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `logs: blaxel.core.client.types.Unset | list[typing.Any]`
    :

    `total_count: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ResourceMetrics(billable_time: blaxel.core.client.types.Unset | ForwardRef('BillableTimeMetric') = <blaxel.core.client.types.Unset object>, inference_errors_global: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, inference_global: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, last_n_requests: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, latency: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, latency_previous: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, memory_allocation: blaxel.core.client.types.Unset | ForwardRef('MemoryAllocationMetric') = <blaxel.core.client.types.Unset object>, model_ttft: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, model_ttft_over_time: blaxel.core.client.types.Unset | ForwardRef('TimeToFirstTokenOverTimeMetrics') = <blaxel.core.client.types.Unset object>, request_duration_over_time: blaxel.core.client.types.Unset | ForwardRef('RequestDurationOverTimeMetrics') = <blaxel.core.client.types.Unset object>, request_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, request_total_by_origin: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetric') = <blaxel.core.client.types.Unset object>, request_total_by_origin_previous: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetric') = <blaxel.core.client.types.Unset object>, request_total_per_code: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRequestTotalPerCode') = <blaxel.core.client.types.Unset object>, request_total_per_code_previous: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRequestTotalPerCodePrevious') = <blaxel.core.client.types.Unset object>, request_total_previous: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps_per_code: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRpsPerCode') = <blaxel.core.client.types.Unset object>, rps_per_code_previous: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRpsPerCodePrevious') = <blaxel.core.client.types.Unset object>, rps_previous: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, sandboxes_cpu_usage: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, sandboxes_ram_usage: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, token_rate: blaxel.core.client.types.Unset | ForwardRef('TokenRateMetrics') = <blaxel.core.client.types.Unset object>, token_total: blaxel.core.client.types.Unset | ForwardRef('TokenTotalMetric') = <blaxel.core.client.types.Unset object>)`
:   Metrics for a single resource deployment (eg. model deployment, function deployment)
    
    Attributes:
        billable_time (Union[Unset, BillableTimeMetric]): Billable time metric
        inference_errors_global (Union[Unset, list['Metric']]): Array of metrics
        inference_global (Union[Unset, list['Metric']]): Array of metrics
        last_n_requests (Union[Unset, list['Metric']]): Array of metrics
        latency (Union[Unset, LatencyMetric]): Latency metrics
        latency_previous (Union[Unset, LatencyMetric]): Latency metrics
        memory_allocation (Union[Unset, MemoryAllocationMetric]): Metrics for memory allocation
        model_ttft (Union[Unset, LatencyMetric]): Latency metrics
        model_ttft_over_time (Union[Unset, TimeToFirstTokenOverTimeMetrics]): Time to first token over time metrics
        request_duration_over_time (Union[Unset, RequestDurationOverTimeMetrics]): Request duration over time metrics
        request_total (Union[Unset, float]): Number of requests for the resource globally
        request_total_by_origin (Union[Unset, RequestTotalByOriginMetric]): Request total by origin metric
        request_total_by_origin_previous (Union[Unset, RequestTotalByOriginMetric]): Request total by origin metric
        request_total_per_code (Union[Unset, ResourceMetricsRequestTotalPerCode]): Number of requests for the resource
            globally per code
        request_total_per_code_previous (Union[Unset, ResourceMetricsRequestTotalPerCodePrevious]): Number of requests
            for the resource globally per code for the previous period
        request_total_previous (Union[Unset, float]): Number of requests for the resource globally for the previous
            period
        rps (Union[Unset, float]): Number of requests per second for the resource globally
        rps_per_code (Union[Unset, ResourceMetricsRpsPerCode]): Number of requests per second for the resource globally
            per code
        rps_per_code_previous (Union[Unset, ResourceMetricsRpsPerCodePrevious]): Number of requests per second for the
            resource globally per code for the previous period
        rps_previous (Union[Unset, float]): Number of requests per second for the resource globally for the previous
            period
        sandboxes_cpu_usage (Union[Unset, list[Any]]): CPU usage over time for sandboxes
        sandboxes_ram_usage (Union[Unset, list[Any]]): RAM usage over time for sandboxes with memory, value, and percent
            metrics
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

    `billable_time`
    :

    `inference_errors_global`
    :

    `inference_global`
    :

    `last_n_requests`
    :

    `latency`
    :

    `latency_previous`
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

    `request_total_by_origin_previous`
    :

    `request_total_per_code`
    :

    `request_total_per_code_previous`
    :

    `request_total_previous`
    :

    `rps`
    :

    `rps_per_code`
    :

    `rps_per_code_previous`
    :

    `rps_previous`
    :

    `sandboxes_cpu_usage`
    :

    `sandboxes_ram_usage`
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

`ResourceMetricsRequestTotalPerCodePrevious()`
:   Number of requests for the resource globally per code for the previous period
    
    Method generated by attrs for class ResourceMetricsRequestTotalPerCodePrevious.

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

`ResourceMetricsRpsPerCodePrevious()`
:   Number of requests per second for the resource globally per code for the previous period
    
    Method generated by attrs for class ResourceMetricsRpsPerCodePrevious.

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

`ResourceTrace(duration: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, has_error: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, start_time: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, status_code: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, trace_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Log for a resource deployment (eg. model deployment, function deployment)
    
    Attributes:
        duration (Union[Unset, int]): Duration in nanoseconds
        has_error (Union[Unset, bool]): Has error
        start_time (Union[Unset, str]): The timestamp of the log
        status_code (Union[Unset, int]): Status code
        trace_id (Union[Unset, str]): Trace ID of the log
    
    Method generated by attrs for class ResourceTrace.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `duration: blaxel.core.client.types.Unset | int`
    :

    `has_error: blaxel.core.client.types.Unset | bool`
    :

    `start_time: blaxel.core.client.types.Unset | str`
    :

    `status_code: blaxel.core.client.types.Unset | int`
    :

    `trace_id: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RevisionConfiguration(active: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, canary: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, canary_percent: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, traffic: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
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

    `active: blaxel.core.client.types.Unset | str`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `canary: blaxel.core.client.types.Unset | str`
    :

    `canary_percent: blaxel.core.client.types.Unset | int`
    :

    `traffic: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RevisionMetadata(active: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, canary: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, previous_active: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, traffic_percent: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
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

    `active: blaxel.core.client.types.Unset | bool`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `canary: blaxel.core.client.types.Unset | bool`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `created_by: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `previous_active: blaxel.core.client.types.Unset | bool`
    :

    `status: blaxel.core.client.types.Unset | str`
    :

    `traffic_percent: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Runtime(args: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, command: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, configuration: blaxel.core.client.types.Unset | ForwardRef('RuntimeConfiguration') = <blaxel.core.client.types.Unset object>, cpu: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, endpoint_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, envs: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, expires: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, generation: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, image: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, max_concurrent_tasks: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, max_retries: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, max_scale: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, memory: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, metric_port: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, min_scale: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, model: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, organization: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ports: blaxel.core.client.types.Unset | list['Port'] = <blaxel.core.client.types.Unset object>, startup_probe: blaxel.core.client.types.Unset | ForwardRef('RuntimeStartupProbe') = <blaxel.core.client.types.Unset object>, timeout: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, ttl: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Set of configurations for a deployment
    
    Attributes:
        args (Union[Unset, list[Any]]): The arguments to pass to the deployment runtime
        command (Union[Unset, list[Any]]): The command to run the deployment
        configuration (Union[Unset, RuntimeConfiguration]): The configuration for the deployment
        cpu (Union[Unset, int]): The CPU for the deployment in cores, only available for private cluster
        endpoint_name (Union[Unset, str]): Endpoint Name of the model. In case of hf_private_endpoint, it is the
            endpoint name. In case of hf_public_endpoint, it is not used.
        envs (Union[Unset, list[Any]]): The env variables to set in the deployment. Should be a list of Kubernetes
            EnvVar types
        expires (Union[Unset, str]): The expiration date for the deployment in ISO 8601 format - 2024-12-31T23:59:59Z
        generation (Union[Unset, str]): The generation of the deployment
        image (Union[Unset, str]): The Docker image for the deployment
        max_concurrent_tasks (Union[Unset, int]): The maximum number of concurrent task for an execution
        max_retries (Union[Unset, int]): The maximum number of retries for the deployment
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
        ttl (Union[Unset, str]): The TTL for the deployment in seconds - 30m, 24h, 7d
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

    `configuration`
    :

    `cpu`
    :

    `endpoint_name`
    :

    `envs`
    :

    `expires`
    :

    `generation`
    :

    `image`
    :

    `max_concurrent_tasks`
    :

    `max_retries`
    :

    `max_scale`
    :

    `memory`
    :

    `metric_port`
    :

    `min_scale`
    :

    `model`
    :

    `organization`
    :

    `ports`
    :

    `startup_probe`
    :

    `timeout`
    :

    `ttl`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`RuntimeConfiguration()`
:   The configuration for the deployment
    
    Method generated by attrs for class RuntimeConfiguration.

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

`Sandbox(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, last_used_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('SandboxSpec') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ttl: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Micro VM for running agentic tasks
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        last_used_at (Union[Unset, str]): Last time the sandbox was used (read-only, managed by the system)
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, SandboxSpec]): Sandbox specification
        status (Union[Unset, str]): Sandbox status
        ttl (Union[Unset, int]): TTL timestamp for automatic deletion (optional, nil means no auto-deletion)
    
    Method generated by attrs for class Sandbox.

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

    `last_used_at`
    :

    `metadata`
    :

    `spec`
    :

    `status`
    :

    `ttl`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SandboxDefinition(categories: blaxel.core.client.types.Unset | list[typing.Any] = <blaxel.core.client.types.Unset object>, coming_soon: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, enterprise: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, icon: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, image: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, long_description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, memory: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ports: blaxel.core.client.types.Unset | list['Port'] = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Sandbox definition for admin store operations
    
    Attributes:
        categories (Union[Unset, list[Any]]): Categories of the defintion
        coming_soon (Union[Unset, bool]): If the definition is coming soon
        description (Union[Unset, str]): Description of the defintion
        display_name (Union[Unset, str]): Display name of the definition
        enterprise (Union[Unset, bool]): If the definition is enterprise
        icon (Union[Unset, str]): Icon of the definition
        image (Union[Unset, str]): Image of the Sandbox definition
        long_description (Union[Unset, str]): Long description of the defintion
        memory (Union[Unset, int]): Memory of the Sandbox definition in MB
        name (Union[Unset, str]): Name of the artifact
        ports (Union[Unset, list['Port']]): Set of ports for a resource
        url (Union[Unset, str]): URL of the definition
    
    Method generated by attrs for class SandboxDefinition.

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

    `description`
    :

    `display_name`
    :

    `enterprise`
    :

    `icon`
    :

    `image`
    :

    `long_description`
    :

    `memory`
    :

    `name`
    :

    `ports`
    :

    `url`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SandboxLifecycle(expiration_policies: blaxel.core.client.types.Unset | list['ExpirationPolicy'] = <blaxel.core.client.types.Unset object>)`
:   Lifecycle configuration for sandbox management
    
    Attributes:
        expiration_policies (Union[Unset, list['ExpirationPolicy']]): List of expiration policies
    
    Method generated by attrs for class SandboxLifecycle.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `expiration_policies`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SandboxMetrics(memory: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, percent: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, value: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
:   Enhanced sandbox metrics with memory, value, and percent data
    
    Attributes:
        memory (Union[Unset, float]): Memory limit in bytes (from query A)
        percent (Union[Unset, float]): Memory usage percentage (from formula F1)
        timestamp (Union[Unset, str]): Metric timestamp
        value (Union[Unset, float]): Memory usage in bytes (from query B)
    
    Method generated by attrs for class SandboxMetrics.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `memory: blaxel.core.client.types.Unset | float`
    :

    `percent: blaxel.core.client.types.Unset | float`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `value: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`SandboxSpec(configurations: blaxel.core.client.types.Unset | ForwardRef('CoreSpecConfigurations') = <blaxel.core.client.types.Unset object>, enabled: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, flavors: blaxel.core.client.types.Unset | list['Flavor'] = <blaxel.core.client.types.Unset object>, integration_connections: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, policies: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, private_clusters: blaxel.core.client.types.Unset | ForwardRef('ModelPrivateCluster') = <blaxel.core.client.types.Unset object>, revision: blaxel.core.client.types.Unset | ForwardRef('RevisionConfiguration') = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('Runtime') = <blaxel.core.client.types.Unset object>, sandbox: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, lifecycle: blaxel.core.client.types.Unset | ForwardRef('SandboxLifecycle') = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, volumes: blaxel.core.client.types.Unset | list['VolumeAttachment'] = <blaxel.core.client.types.Unset object>)`
:   Sandbox specification
    
    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the resource
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        lifecycle (Union[Unset, SandboxLifecycle]): Lifecycle configuration for sandbox management
        region (Union[Unset, str]): Region where the sandbox should be created (e.g. us-pdx-1, eu-lon-1)
        volumes (Union[Unset, list['VolumeAttachment']]):
    
    Method generated by attrs for class SandboxSpec.

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

    `lifecycle`
    :

    `policies`
    :

    `private_clusters`
    :

    `region`
    :

    `revision`
    :

    `runtime`
    :

    `sandbox`
    :

    `volumes`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ServerlessConfig(configuration: blaxel.core.client.types.Unset | ForwardRef('ServerlessConfigConfiguration') = <blaxel.core.client.types.Unset object>, max_retries: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, max_scale: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, min_scale: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, timeout: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Configuration for a serverless deployment
    
    Attributes:
        configuration (Union[Unset, ServerlessConfigConfiguration]): The configuration for the deployment
        max_retries (Union[Unset, int]): The maximum number of retries for the deployment
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

    `additional_properties`
    :

    `configuration`
    :

    `max_retries`
    :

    `max_scale`
    :

    `min_scale`
    :

    `timeout`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`ServerlessConfigConfiguration()`
:   The configuration for the deployment
    
    Method generated by attrs for class ServerlessConfigConfiguration.

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

`SpecConfiguration(secret: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, value: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `secret: blaxel.core.client.types.Unset | bool`
    :

    `value: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StartSandbox(message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Response when starting a Sandbox
    
    Attributes:
        message (Union[Unset, str]): Human readable message about the start operation
        metadata (Union[Unset, Metadata]): Metadata
        status (Union[Unset, str]): Status of the Sandbox start operation
    
    Method generated by attrs for class StartSandbox.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `message`
    :

    `metadata`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StopSandbox(message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Response when stopping a Sandbox
    
    Attributes:
        message (Union[Unset, str]): Human readable message about the stop operation
        metadata (Union[Unset, Metadata]): Metadata
        status (Union[Unset, str]): Status of the Sandbox stop operation
    
    Method generated by attrs for class StopSandbox.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `message`
    :

    `metadata`
    :

    `status`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`StoreAgent(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, configuration: blaxel.core.client.types.Unset | list['StoreConfiguration'] = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, image: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, labels: blaxel.core.client.types.Unset | ForwardRef('StoreAgentLabels') = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, prompt: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`StoreConfiguration(available_models: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, if_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, options: blaxel.core.client.types.Unset | list['StoreConfigurationOption'] = <blaxel.core.client.types.Unset object>, required: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, secret: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

`StoreConfigurationOption(if_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, label: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, value: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `if_: blaxel.core.client.types.Unset | str`
    :

    `label: blaxel.core.client.types.Unset | str`
    :

    `value: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Template(default_branch: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, download_count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, forks_count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, icon: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, icon_dark: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sha: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, star_count: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, topics: blaxel.core.client.types.Unset | list[str] = <blaxel.core.client.types.Unset object>, url: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, variables: blaxel.core.client.types.Unset | list['TemplateVariable'] = <blaxel.core.client.types.Unset object>)`
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

`TemplateVariable(description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, integration: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, path: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, secret: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>)`
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

    `description: blaxel.core.client.types.Unset | str`
    :

    `integration: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `path: blaxel.core.client.types.Unset | str`
    :

    `secret: blaxel.core.client.types.Unset | bool`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TimeFields(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TimeToFirstTokenOverTimeMetrics(time_to_first_token_over_time: blaxel.core.client.types.Unset | ForwardRef('RequestDurationOverTimeMetric') = <blaxel.core.client.types.Unset object>)`
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

`TokenRateMetric(model: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, provider: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, provider_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, timestamp: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, token_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, trend: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `model: blaxel.core.client.types.Unset | str`
    :

    `provider: blaxel.core.client.types.Unset | str`
    :

    `provider_name: blaxel.core.client.types.Unset | str`
    :

    `timestamp: blaxel.core.client.types.Unset | str`
    :

    `token_total: blaxel.core.client.types.Unset | float`
    :

    `trend: blaxel.core.client.types.Unset | float`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TokenRateMetrics(token_rate: blaxel.core.client.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.core.client.types.Unset object>, token_rate_input: blaxel.core.client.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.core.client.types.Unset object>, token_rate_output: blaxel.core.client.types.Unset | ForwardRef('TokenRateMetric') = <blaxel.core.client.types.Unset object>)`
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

`TokenTotalMetric(average_token_input_per_request: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, average_token_output_per_request: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, average_token_per_request: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, token_input: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, token_output: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, token_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>)`
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

    `average_token_input_per_request: blaxel.core.client.types.Unset | float`
    :

    `average_token_output_per_request: blaxel.core.client.types.Unset | float`
    :

    `average_token_per_request: blaxel.core.client.types.Unset | float`
    :

    `token_input: blaxel.core.client.types.Unset | float`
    :

    `token_output: blaxel.core.client.types.Unset | float`
    :

    `token_total: blaxel.core.client.types.Unset | float`
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

`Trigger(configuration: blaxel.core.client.types.Unset | ForwardRef('TriggerConfiguration') = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, type_: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Trigger configuration
    
    Attributes:
        configuration (Union[Unset, TriggerConfiguration]): Trigger configuration
        id (Union[Unset, str]): The id of the trigger
        type_ (Union[Unset, str]): The type of trigger, can be http or http-async
    
    Method generated by attrs for class Trigger.

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

    `id`
    :

    `type_`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TriggerConfiguration(authentication_type: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, path: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, retry: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, schedule: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, tasks: blaxel.core.client.types.Unset | list['TriggerConfigurationTask'] = <blaxel.core.client.types.Unset object>)`
:   Trigger configuration
    
    Attributes:
        authentication_type (Union[Unset, str]): The authentication type of the trigger
        path (Union[Unset, str]): The path of the trigger
        retry (Union[Unset, int]): The retry of the trigger
        schedule (Union[Unset, str]): The schedule of the trigger, cron expression * * * * *
        tasks (Union[Unset, list['TriggerConfigurationTask']]): The tasks configuration of the cronjob
    
    Method generated by attrs for class TriggerConfiguration.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties`
    :

    `authentication_type`
    :

    `path`
    :

    `retry`
    :

    `schedule`
    :

    `tasks`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`TriggerConfigurationTask()`
:   The tasks configuration of the cronjob
    
    Method generated by attrs for class TriggerConfigurationTask.

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

`UpdateWorkspaceServiceAccountBody(description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`UpdateWorkspaceServiceAccountResponse200(client_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, description: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `client_id: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `description: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
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

`Volume(events: blaxel.core.client.types.Unset | list['CoreEvent'] = <blaxel.core.client.types.Unset object>, metadata: blaxel.core.client.types.Unset | ForwardRef('Metadata') = <blaxel.core.client.types.Unset object>, spec: blaxel.core.client.types.Unset | ForwardRef('VolumeSpec') = <blaxel.core.client.types.Unset object>, state: blaxel.core.client.types.Unset | ForwardRef('VolumeState') = <blaxel.core.client.types.Unset object>, status: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, terminated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Volume resource for persistent storage
    
    Attributes:
        events (Union[Unset, list['CoreEvent']]): Core events
        metadata (Union[Unset, Metadata]): Metadata
        spec (Union[Unset, VolumeSpec]): Volume specification - immutable configuration
        state (Union[Unset, VolumeState]): Volume state - mutable runtime state
        status (Union[Unset, str]): Volume status computed from events
        terminated_at (Union[Unset, str]): Timestamp when the volume was marked for termination
    
    Method generated by attrs for class Volume.

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

    `state`
    :

    `status`
    :

    `terminated_at`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`VolumeAttachment(mount_path: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, read_only: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>)`
:   Volume attachment configuration for sandbox
    
    Attributes:
        mount_path (Union[Unset, str]): Mount path in the container
        name (Union[Unset, str]): Name of the volume to attach
        read_only (Union[Unset, bool]): Whether the volume is mounted as read-only
    
    Method generated by attrs for class VolumeAttachment.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `mount_path: blaxel.core.client.types.Unset | str`
    :

    `name: blaxel.core.client.types.Unset | str`
    :

    `read_only: blaxel.core.client.types.Unset | bool`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`VolumeSpec(region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, size: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>)`
:   Volume specification - immutable configuration
    
    Attributes:
        region (Union[Unset, str]): Region where the volume should be created (e.g. us-pdx-1, eu-lon-1)
        size (Union[Unset, int]): Size of the volume in MB
    
    Method generated by attrs for class VolumeSpec.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `region: blaxel.core.client.types.Unset | str`
    :

    `size: blaxel.core.client.types.Unset | int`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`VolumeState(attached_to: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Volume state - mutable runtime state
    
    Attributes:
        attached_to (Union[Unset, str]): Resource this volume is attached to (e.g. "sandbox:my-sandbox", "model:my-
            model")
    
    Method generated by attrs for class VolumeState.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `attached_to: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WebsocketChannel(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, connection_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `connection_id: blaxel.core.client.types.Unset | str`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WebsocketMessage(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, message: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, ttl: blaxel.core.client.types.Unset | int = <blaxel.core.client.types.Unset object>, workspace: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   WebSocket connection details
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        id (Union[Unset, str]): Unique message ID
        message (Union[Unset, str]): Message
        ttl (Union[Unset, int]): TTL timestamp for automatic deletion
        workspace (Union[Unset, str]): Workspace the connection belongs to
    
    Method generated by attrs for class WebsocketMessage.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `created_at: blaxel.core.client.types.Unset | str`
    :

    `id: blaxel.core.client.types.Unset | str`
    :

    `message: blaxel.core.client.types.Unset | str`
    :

    `ttl: blaxel.core.client.types.Unset | int`
    :

    `updated_at: blaxel.core.client.types.Unset | str`
    :

    `workspace: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`Workspace(created_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_at: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, created_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, updated_by: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, account_id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, display_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, id: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, labels: blaxel.core.client.types.Unset | ForwardRef('WorkspaceLabels') = <blaxel.core.client.types.Unset object>, name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, region: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, runtime: blaxel.core.client.types.Unset | ForwardRef('WorkspaceRuntime') = <blaxel.core.client.types.Unset object>)`
:   Workspace
    
    Attributes:
        created_at (Union[Unset, str]): The date and time when the resource was created
        updated_at (Union[Unset, str]): The date and time when the resource was updated
        created_by (Union[Unset, str]): The user or service account who created the resource
        updated_by (Union[Unset, str]): The user or service account who updated the resource
        account_id (Union[Unset, str]): Workspace account id
        display_name (Union[Unset, str]): Workspace display name
        id (Union[Unset, str]): Autogenerated unique workspace id
        labels (Union[Unset, WorkspaceLabels]): Workspace labels
        name (Union[Unset, str]): Workspace name
        region (Union[Unset, str]): Workspace write region
        runtime (Union[Unset, WorkspaceRuntime]): Workspace runtime
    
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

    `id`
    :

    `labels`
    :

    `name`
    :

    `region`
    :

    `runtime`
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

`WorkspaceRuntime(generation: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
:   Workspace runtime
    
    Attributes:
        generation (Union[Unset, str]): Workspace generation
    
    Method generated by attrs for class WorkspaceRuntime.

    ### Static methods

    `from_dict(src_dict: dict[str, typing.Any]) ‑> ~T`
    :

    ### Instance variables

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `generation: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :

`WorkspaceUser(accepted: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, email: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, email_verified: blaxel.core.client.types.Unset | bool = <blaxel.core.client.types.Unset object>, family_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, given_name: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, role: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>, sub: blaxel.core.client.types.Unset | str = <blaxel.core.client.types.Unset object>)`
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

    `accepted: blaxel.core.client.types.Unset | bool`
    :

    `additional_keys: list[str]`
    :

    `additional_properties: dict[str, typing.Any]`
    :

    `email: blaxel.core.client.types.Unset | str`
    :

    `email_verified: blaxel.core.client.types.Unset | bool`
    :

    `family_name: blaxel.core.client.types.Unset | str`
    :

    `given_name: blaxel.core.client.types.Unset | str`
    :

    `role: blaxel.core.client.types.Unset | str`
    :

    `sub: blaxel.core.client.types.Unset | str`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :