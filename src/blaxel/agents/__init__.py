import json
from logging import getLogger
from typing import Any, Awaitable

from ..cache import find_from_cache
from ..client import client
from ..client.api.agents import get_agent
from ..client.models import Agent
from ..common.env import env
from ..common.internal import get_global_unique_hash
from ..common.settings import settings
from ..instrumentation.span import SpanManager

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
        env_var = self.name.replace("-", "_").upper()
        if env[f"BL_AGENT_{env_var}_URL"]:
            return env[f"BL_AGENT_{env_var}_URL"]
        return None

    @property
    def external_url(self):
        return f"{settings.run_url}/{settings.workspace}/agents/{self.name}"

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

        return client.get_httpx_client().post(
            url,
            headers={
                'Content-Type': 'application/json',
                **headers
            },
            data=body,
            params=params
        )

    async def acall(self, url, input_data, headers: dict = {}, params: dict = {}):
        logger.debug(f"Agent Calling: {self.name}")
        body = input_data
        if not isinstance(body, str):
            body = json.dumps(body)

        return await client.get_async_httpx_client().post(
            url,
            headers={
                'Content-Type': 'application/json',
                **headers
            },
            data=body,
            params=params
        )

    def run(self, input: Any, headers: dict = {}, params: dict = {}) -> str:
        attributes = {
            "agent.name": self.name,
            "agent.args": json.dumps(input),
            "span.type": "agent.run",
        }
        with SpanManager("blaxel-tracer").create_active_span(self.name, attributes) as span:
            logger.debug(f"Agent Calling: {self.name}")
            response = self.call(self.url, input, headers, params)
            if response.status_code >= 400:
                if not self.fallback_url:
                    span.set_attribute("agent.run.error", response.text)
                    raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
                response = self.call(self.fallback_url, input, headers, params)
                if response.status_code >= 400:
                    span.set_attribute("agent.run.error", response.text)
                    raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
            span.set_attribute("agent.run.result", response.text)
            return response.text

    async def arun(self, input: Any, headers: dict = {}, params: dict = {}) -> Awaitable[str]:
        attributes = {
            "agent.name": self.name,
            "agent.args": json.dumps(input),
            "span.type": "agent.run",
        }
        with SpanManager("blaxel-tracer").create_active_span(self.name, attributes) as span:
            logger.debug(f"Agent Calling: {self.name}")
            response = await self.acall(self.url, input, headers, params)
            if response.status_code >= 400:
                if not self.fallback_url:
                    span.set_attribute("agent.run.error", response.text)
                    raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
                response = await self.acall(self.fallback_url, input, headers, params)
                if response.status_code >= 400:
                    span.set_attribute("agent.run.error", response.text)
                    raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
            span.set_attribute("agent.run.result", response.text)
            return response.text

    def __str__(self):
        return f"Agent {self.name}"

    def __repr__(self):
        return self.__str__()

def bl_agent(name: str):
    return BlAgent(name)

async def get_agent_metadata(name):
    cache_data = await find_from_cache('Agent', name)
    if cache_data:
        return Agent.from_dict(cache_data)
    try:
        return await get_agent.asyncio(client=client, agent_name=name)
    except Exception:
        return None
