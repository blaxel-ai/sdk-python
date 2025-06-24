Module blaxel.telemetry.instrumentation.blaxel_langgraph_gemini
===============================================================
OpenTelemetry Google Generative AI API instrumentation

Functions
---------

`is_async_streaming_response(response)`
:   

`is_streaming_response(response)`
:   

`should_send_prompts()`
:   

Classes
-------

`BlaxelLanggraphGeminiInstrumentor(exception_logger=None)`
:   An instrumentor for Google Generative AI's client library.

    ### Ancestors (in MRO)

    * opentelemetry.instrumentation.instrumentor.BaseInstrumentor
    * abc.ABC

    ### Methods

    `instrumentation_dependencies(self) ‑> Collection[str]`
    :   Return a list of python packages with versions that the will be instrumented.
        
        The format should be the same as used in requirements.txt or pyproject.toml.
        
        For example, if an instrumentation instruments requests 1.x, this method should look
        like:
        
            def instrumentation_dependencies(self) -> Collection[str]:
                return ['requests ~= 1.0']
        
        This will ensure that the instrumentation will only be used when the specified library
        is present in the environment.