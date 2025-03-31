import nest_asyncio

# This is because crewai is not asyncio compatible for now: https://github.com/crewAIInc/crewAI/issues/195
nest_asyncio.apply()

import asyncio
from contextlib import asynccontextmanager
from logging import getLogger

import uvicorn
from crewai import Agent, Crew, Task
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import StreamingResponse

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

async def main():
    router = APIRouter()

    async with bl_tools(["blaxel-search"]) as t:
        tools = t.to_crewai()
        model = await bl_model("gpt-4o-mini").to_crewai()
        agent = Agent(
            role="Weather Researcher",
            goal="Find the weather in a specific city",
            backstory="You are an experienced weather researcher with attention to detail",
            llm=model,
            tools=tools,
            verbose=True,
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            logger.info("Server running on port 1338")
            yield
            logger.info("Server shutting down")


        @router.post("/")
        async def handle_request(request: Request):
            body = await request.json()
            crew = Crew(
                agents=[agent],
                tasks=[
                    Task(
                        description=body.get("description", "Find the weather in a specific city"),
                        expected_output=body.get("expected_output", "Weather in San francisco."),
                        agent=agent
                    )
                ],
                verbose=True,
            )
            result = crew.kickoff()
            # Process the message with your run function
            return StreamingResponse(
                result.raw,
                media_type="text/plain"
            )

        app = FastAPI(lifespan=lifespan)
        app.include_router(router)
        uvicorn.run(app, host="0.0.0.0", port=1338)

if __name__ == "__main__":
    asyncio.run(main())
