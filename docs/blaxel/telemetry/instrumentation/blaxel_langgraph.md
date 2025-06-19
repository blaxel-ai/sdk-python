Module blaxel.telemetry.instrumentation.blaxel_langgraph
========================================================

Classes
-------

`BlaxelLanggraphInstrumentor(*args, **kwargs)`
:   An ABC for instrumentors.
    
    Child classes of this ABC should instrument specific third
    party libraries or frameworks either by using the
    ``opentelemetry-instrument`` command or by calling their methods
    directly.
    
    Since every third party library or framework is different and has different
    instrumentation needs, more methods can be added to the child classes as
    needed to provide practical instrumentation to the end user.

    ### Ancestors (in MRO)

    * opentelemetry.instrumentation.instrumentor.BaseInstrumentor
    * abc.ABC

    ### Methods

    `instrumentation_dependencies(self)`
    :   Return a list of python packages with versions that the will be instrumented.
        
        The format should be the same as used in requirements.txt or pyproject.toml.
        
        For example, if an instrumentation instruments requests 1.x, this method should look
        like:
        
            def instrumentation_dependencies(self) -> Collection[str]:
                return ['requests ~= 1.0']
        
        This will ensure that the instrumentation will only be used when the specified library
        is present in the environment.