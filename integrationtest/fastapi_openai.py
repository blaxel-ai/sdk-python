import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from agents import Agent, Runner
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import StreamingResponse

from blaxel.models import bl_model
from blaxel.tools import BlTools

logger = getLogger(__name__)

async def main():
    router = APIRouter()

    async with BlTools(["blaxel-search"]) as bl_tools:
        tools = bl_tools.to_openai()
        model = await bl_model("gpt-4o-mini").to_openai()
        agent = Agent(
            name="blaxel-agent",
            model=model,
            tools=tools,
            instructions="You are a helpful assistant. Maximum number of tool call is 1",
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Server running on port 1338")
            yield
            logger.info("Server shutting down")


        @router.post("/")
        async def handle_request(request: Request):
            body = await request.json()
            result = await Runner.run(agent, body.get("input", ""))
            return StreamingResponse(
                result.final_output,
                media_type="text/plain"
            )

        app = FastAPI(lifespan=lifespan)
        app.include_router(router)
        server = uvicorn.Server(uvicorn.Config(app=app, host="0.0.0.0", port=1338))
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
