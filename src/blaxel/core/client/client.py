import asyncio
import ssl
from typing import Any, Union

import httpx
from attrs import define, evolve, field


@define
class Client:
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``auth``: An implementation of httpx.Auth to use for authentication

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
        auth: Auth to use for authentication
    """

    raise_on_unexpected_status: bool = field(default=True, kw_only=True)
    _base_url: str = field(alias="base_url", default="")
    _cookies: dict[str, str] = field(factory=dict, kw_only=True, alias="cookies")
    _headers: dict[str, str] = field(factory=dict, kw_only=True, alias="headers")
    _auth: httpx.Auth = field(default=None, alias="auth")
    _timeout: httpx.Timeout | None = field(default=None, kw_only=True, alias="timeout")
    _verify_ssl: Union[str, bool, ssl.SSLContext] = field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = field(default=False, kw_only=True, alias="follow_redirects")
    _httpx_args: dict[str, Any] = field(factory=dict, kw_only=True, alias="httpx_args")
    _client: httpx.Client | None = field(default=None, init=False)
    _async_client: httpx.AsyncClient | None = field(default=None, init=False)
    _async_client_loop: asyncio.AbstractEventLoop | None = field(default=None, init=False)

    def with_base_url(self, base_url: str) -> "Client":
        """Get a new client matching this one with a new base URL"""
        self._base_url = base_url
        if self._client is not None:
            self._client.base_url = base_url
        if self._async_client is not None:
            self._async_client.base_url = base_url
        return evolve(self, base_url=base_url)

    def with_headers(self, headers: dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        self._headers = headers
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        self._cookies = cookies
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        self._timeout = timeout
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def with_auth(self, auth: httpx.Auth) -> "Client":
        """Get a new client matching this one with a new provider"""
        self._auth = auth
        if self._client is not None:
            self._client.auth = auth
        if self._async_client is not None:
            self._async_client.auth = auth
        return evolve(self, auth=auth)

    def set_httpx_client(self, client: httpx.Client) -> "Client":
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                auth=self._auth,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set.
        
        Automatically detects event loop changes and recreates the client if needed.
        This prevents "Event loop is closed" errors when tests run in parallel.
        """
        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop running, return existing client or create new one
            current_loop = None
        
        # Check if we need to recreate the client due to event loop change
        needs_recreation = False
        if self._async_client is not None:
            # Client exists, check if it's still valid
            if current_loop is not None and self._async_client_loop is not current_loop:
                # Different event loop, need to close old client and create new one
                needs_recreation = True
            elif self._async_client.is_closed:
                # Client was closed, need new one
                needs_recreation = True
        
        if needs_recreation:
            # Close old client (best effort, ignore errors)
            try:
                # Can't await here since we're not async, but mark for garbage collection
                self._async_client = None
                self._async_client_loop = None
            except Exception:
                pass
        
        if self._async_client is None:
            # Configure connection limits to help with event loop cleanup issues in tests
            # Use smaller limits to ensure connections are closed promptly
            limits = httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
                keepalive_expiry=5.0,  # Close idle connections after 5 seconds
            )
            
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                auth=self._auth,
                limits=limits,
                **self._httpx_args,
            )
            self._async_client_loop = current_loop
            
        return self._async_client

    async def __aenter__(self) -> "Client":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)


client = Client()
