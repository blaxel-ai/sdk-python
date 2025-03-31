import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import StreamingResponse
from llama_index.core.agent.workflow import (AgentOutput, ReActAgent,
                                             ToolCallResult)
from llama_index.core.workflow import Context

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def main():
    router = APIRouter()

    async with bl_tools(["blaxel-search"]) as t:
        tools = t.to_llamaindex()
        model = await bl_model("gpt-4o-mini").to_llamaindex()
        agent = ReActAgent(llm=model, tools=tools, system_prompt="You are a helpful assistant. Maximum number of tool call is 1.")
        context = Context(agent)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Server running on port 1338")
            yield
            logger.info("Server shutting down")


        @router.post("/")
        async def handle_request(request: Request):
            body = await request.json()
            handler = agent.run(body.get("input", ""), ctx=context)
            async for ev in handler.stream_events():
                if isinstance(ev, ToolCallResult):
                    logger.info(f"Call {ev.tool_name} with {ev.tool_kwargs}")
            response: AgentOutput = await handler
            return StreamingResponse(
                response.response.blocks[-1].text,
                media_type="text/plain"
            )

        app = FastAPI(lifespan=lifespan)
        app.include_router(router)
        server = uvicorn.Server(uvicorn.Config(app=app, host="0.0.0.0", port=1338))
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
