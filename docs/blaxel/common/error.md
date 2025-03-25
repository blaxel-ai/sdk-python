Module blaxel.common.error
==========================
This module defines custom exception classes used for handling HTTP-related errors within Blaxel.

Classes
-------

`HTTPError(status_code: int, message: str)`
:   A custom exception class for HTTP errors.
    
    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (str): A descriptive message explaining the error.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException