
import json
from logging import getLogger
from typing import Any, Awaitable

from ..cache import find_from_cache
from ..client import client
from ..client.api.agents import get_agent
from ..client.models import Agent
from ..common.env import env
from ..common.settings import settings
from ..instrumentation.span import SpanManager

logger = getLogger(__name__)

class BlAgent:
    def __init__(self, name: str):
        self.name = name


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
        env_var = self.name.replace("-", "_").upper()
        if env[f"BL_AGENT_{env_var}_URL"]:
            return env[f"BL_AGENT_{env_var}_URL"]
        if f"BL_AGENT_{env_var}_SERVICE_NAME" in settings.env:
            return f"https://{settings.env[f'BL_AGENT_{env_var}_SERVICE_NAME']}.{settings.run_internal_hostname}"
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

    async def acall(self, input_data, headers: dict = {}, params: dict = {}):
        logger.debug(f"Agent Calling: {self.name}")
        body = input_data
        if not isinstance(body, str):
            body = json.dumps(body)

        return await client.get_async_httpx_client().post(
            self.url,
            headers={
                'Content-Type': 'application/json',
                **headers
            },
            data=body,
            params=params
        )

    def run(self, input: Any, headers: dict = {}, params: dict = {}) -> str:
        with SpanManager("blaxel-tracer").create_active_span(self.name, {"agent.name": self.name, "agent.args": json.dumps(input)}):
            logger.debug(f"Agent Calling: {self.name}")
            response = self.call(self.url, input, headers, params)
            if response.status_code >= 400:
                raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
            return response.text

    async def arun(self, input: Any, headers: dict = {}, params: dict = {}) -> Awaitable[str]:
        logger.debug(f"Agent Calling: {self.name}")
        response = await self.acall(input, headers, params)
        if response.status_code >= 400:
            raise Exception(f"Agent {self.name} returned status code {response.status_code} with body {response.text}")
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
    except Exception as e:
        return None
