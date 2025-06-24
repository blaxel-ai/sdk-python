Module blaxel.core.client.models.resource_metrics
=================================================

Classes
-------

`ResourceMetrics(billable_time: blaxel.core.client.types.Unset | ForwardRef('BillableTimeMetric') = <blaxel.core.client.types.Unset object>, inference_errors_global: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, inference_global: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, last_n_requests: blaxel.core.client.types.Unset | list['Metric'] = <blaxel.core.client.types.Unset object>, latency: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, latency_previous: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, memory_allocation: blaxel.core.client.types.Unset | ForwardRef('MemoryAllocationMetric') = <blaxel.core.client.types.Unset object>, model_ttft: blaxel.core.client.types.Unset | ForwardRef('LatencyMetric') = <blaxel.core.client.types.Unset object>, model_ttft_over_time: blaxel.core.client.types.Unset | ForwardRef('TimeToFirstTokenOverTimeMetrics') = <blaxel.core.client.types.Unset object>, request_duration_over_time: blaxel.core.client.types.Unset | ForwardRef('RequestDurationOverTimeMetrics') = <blaxel.core.client.types.Unset object>, request_total: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, request_total_by_origin: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetric') = <blaxel.core.client.types.Unset object>, request_total_by_origin_previous: blaxel.core.client.types.Unset | ForwardRef('RequestTotalByOriginMetric') = <blaxel.core.client.types.Unset object>, request_total_per_code: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRequestTotalPerCode') = <blaxel.core.client.types.Unset object>, request_total_per_code_previous: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRequestTotalPerCodePrevious') = <blaxel.core.client.types.Unset object>, request_total_previous: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, rps_per_code: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRpsPerCode') = <blaxel.core.client.types.Unset object>, rps_per_code_previous: blaxel.core.client.types.Unset | ForwardRef('ResourceMetricsRpsPerCodePrevious') = <blaxel.core.client.types.Unset object>, rps_previous: blaxel.core.client.types.Unset | float = <blaxel.core.client.types.Unset object>, token_rate: blaxel.core.client.types.Unset | ForwardRef('TokenRateMetrics') = <blaxel.core.client.types.Unset object>, token_total: blaxel.core.client.types.Unset | ForwardRef('TokenTotalMetric') = <blaxel.core.client.types.Unset object>)`
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

    `token_rate`
    :

    `token_total`
    :

    ### Methods

    `to_dict(self) ‑> dict[str, typing.Any]`
    :