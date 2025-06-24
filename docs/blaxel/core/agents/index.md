Module blaxel.core.agents
=========================

Functions
---------

`bl_agent(name: str)`
:   

`get_agent_metadata(name)`
:   

Classes
-------

`BlAgent(name: str)`
:   

    ### Instance variables

    `external_url`
    :

    `fallback_url`
    :

    `forced_url`
    :   Get the forced URL from environment variables if set.

    `internal_url`
    :   Get the internal URL for the agent using a hash of workspace and agent name.

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