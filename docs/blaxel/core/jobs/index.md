Module blaxel.core.jobs
=======================

Functions
---------

`bl_job(name: str)`
:   

Classes
-------

`BlJob(name: str)`
:   

    ### Instance variables

    `external_url`
    :

    `fallback_url`
    :

    `forced_url`
    :   Get the forced URL from environment variables if set.

    `internal_url`
    :   Get the internal URL for the job using a hash of workspace and job name.

    `url`
    :

    ### Methods

    `acall(self, url, input_data, headers: dict = {}, params: dict = {})`
    :

    `arun(self, input: Any, headers: dict = {}, params: dict = {}) ‑> Awaitable[str]`
    :

    `call(self, url, input_data, headers: dict = {}, params: dict = {})`
    :

    `run(self, input: Any, headers: dict = {}, params: dict = {}) ‑> str`
    :

`BlJobWrapper()`
:   

    ### Instance variables

    `index: int`
    :

    `index_key: str`
    :

    ### Methods

    `get_arguments(self) ‑> Dict[str, Any]`
    :

    `start(self, func: Callable)`
    :   Run a job defined in a function, it's run in the current process.
        Handles both async and sync functions.
        Arguments are passed as keyword arguments to the function.