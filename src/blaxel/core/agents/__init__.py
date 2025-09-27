import json
from logging import getLogger
from typing import Any, Awaitable

from ..cache import find_from_cache
from ..client import client
from ..client.api.agents import get_agent
from ..client.models import Agent
from ..common.internal import get_forced_url, get_global_unique_hash
from ..common.settings import settings

logger = getLogger(__name__)


class BlAgent:
    def __init__(self, name: str):
        self.name = name

    @property
    def internal_url(self):
        """Get the internal URL for the agent using a hash of workspace and agent name."""
        hash = get_global_unique_hash(settings.workspace, "agent", self.name)
        return f"{settings.run_internal_protocol}://bl-{settings.env}-{hash}.{settings.run_internal_hostname}"

    @property
    def forced_url(self):
        """Get the forced URL from environment variables if set."""
        return get_forced_url("agent", self.name)

    @property
    def external_url(self):
        # Try to get metadata URL asynchronously (this is a sync property so we can't await)
        # The metadata URL will be used in async methods instead
        return f"{settings.run_url}/{settings.workspace}/agents/{self.name}"
    
    async def _get_metadata_url(self):
        """Get URL from agent metadata if available."""
        try:
            metadata = await get_agent_metadata(self.name)
            if metadata:
                # Check if URL is directly in metadata (like TypeScript: metadata?.url)
                if 'url' in metadata and metadata['url']:
                    return metadata['url']
                
                # Check if URL is in nested metadata object
                if hasattr(metadata, 'metadata') and metadata.metadata and 'url' in metadata.metadata:
                    return metadata.metadata['url']
        except Exception:
            pass
        return None
    
    async def get_effective_url(self):
        """Get the effective URL to use, checking metadata first."""
        if self.forced_url:
            return self.forced_url
        
        # Try to get metadata URL
        metadata_url = await self._get_metadata_url()
        if metadata_url:
            return metadata_url
            
        if settings.run_internal_hostname:
            return self.internal_url
        
        return self.external_url

    @property
    def fallback_url(self):
        if self.external_url != self.url:
            return self.external_url
        return None

    @property
    def url(self):
        if self.forced_url:
            return self.forced_url
        if settings.run_internal_hostname:
            return self.internal_url
        return self.external_url

    def call(self, url, input_data, headers: dict = {}, params: dict = {}):
        body = input_data
        if not isinstance(body, str):
            body = json.dumps(body)
        
        # Merge settings headers with provided headers
        merged_headers = {**settings.headers, "Content-Type": "application/json", **headers}

        return client.get_httpx_client().post(
            url, headers=merged_headers, data=body, params=params
        )

    async def acall(self, url, input_data, headers: dict = {}, params: dict = {}):
        logger.debug(f"Agent Calling: {self.name}")
        body = input_data
        if not isinstance(body, str):
            body = json.dumps(body)
        
        # Merge settings headers with provided headers
        merged_headers = {**settings.headers, "Content-Type": "application/json", **headers}

        return await client.get_async_httpx_client().post(
            url, headers=merged_headers, data=body, params=params
        )

    def run(self, input: Any, headers: dict = {}, params: dict = {}) -> str:
        logger.debug(f"Agent Calling: {self.name}")
        response = self.call(self.url, input, headers, params)
        if response.status_code >= 400:
            if not self.fallback_url:
                raise Exception(
                    f"Agent {self.name} returned status code {response.status_code} with body {response.text}"
                )
            response = self.call(self.fallback_url, input, headers, params)
            if response.status_code >= 400:
                raise Exception(
                    f"Agent {self.name} returned status code {response.status_code} with body {response.text}"
                )
        return response.text

    async def arun(self, input: Any, headers: dict = {}, params: dict = {}) -> Awaitable[str]:
        logger.debug(f"Agent Calling: {self.name}")
        effective_url = await self.get_effective_url()
        response = await self.acall(effective_url, input, headers, params)
        if response.status_code >= 400:
            if not self.fallback_url:
                raise Exception(
                    f"Agent {self.name} returned status code {response.status_code} with body {response.text}"
                )
            response = await self.acall(self.fallback_url, input, headers, params)
            if response.status_code >= 400:
                raise Exception(
                    f"Agent {self.name} returned status code {response.status_code} with body {response.text}"
                )
        return response.text

    def __str__(self):
        return f"Agent {self.name}"

    def __repr__(self):
        return self.__str__()


def bl_agent(name: str):
    return BlAgent(name)


async def get_agent_metadata(name):
    cache_data = await find_from_cache("Agent", name)
    if cache_data:
        return Agent.from_dict(cache_data)
    try:
        return await get_agent.asyncio(client=client, agent_name=name)
    except Exception:
        return None
