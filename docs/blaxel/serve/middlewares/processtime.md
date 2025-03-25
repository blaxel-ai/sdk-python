Module blaxel.serve.middlewares.processtime
===========================================
Module: processtime

Defines the AddProcessTimeHeader middleware for adding process time information to responses.

Classes
-------

`AddProcessTimeHeader(app: ASGIApp, dispatch: DispatchFunction | None = None)`
:   Middleware to add the X-Process-Time header to each HTTP response.

    ### Ancestors (in MRO)

    * starlette.middleware.base.BaseHTTPMiddleware

    ### Methods

    `dispatch(self, request, call_next)`
    :   Calculates and adds the processing time to the response headers.
        
        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or endpoint handler.
        
        Returns:
            Response: The HTTP response with the X-Process-Time header added.