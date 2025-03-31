import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def main():
    router = APIRouter()

    async with bl_tools(["blaxel-search"]) as t:
        tools = t.to_langchain()
        model = await bl_model("gpt-4o-mini").to_langchain()
        agent = create_react_agent(model=model, tools=tools, prompt="You are a helpful assistant that can answer questions and help with tasks.")

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Server running on port 1338")
            yield
            logger.info("Server shutting down")


        @router.post("/")
        async def handle_request(request: Request):
            body = await request.json()
            result = await agent.ainvoke({"messages": [HumanMessage(body.get("input", ""))]})
            return StreamingResponse(
                result["messages"][-1].content,
                media_type="text/plain"
            )

        app = FastAPI(lifespan=lifespan)
        app.include_router(router)
        server = uvicorn.Server(uvicorn.Config(app=app, host="0.0.0.0", port=1338))
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
