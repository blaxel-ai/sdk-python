Module blaxel.errors
====================
Contains shared errors types that can be raised from API functions

Classes
-------

`UnexpectedStatus(status_code: int, content: bytes)`
:   Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException