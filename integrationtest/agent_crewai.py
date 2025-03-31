
import nest_asyncio

nest_asyncio.apply()
import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from crewai import Agent, Crew, Task

from blaxel.models import bl_model
from blaxel.tools import BlTools

logger = getLogger(__name__)

async def main():
    async with BlTools(["blaxel-search"]) as bl_tools:
        tools = bl_tools.to_crewai()
        model = await bl_model("gpt-4o-mini").to_crewai()

        agent = Agent(
            role="Weather Researcher",
            goal="Find the weather in a specific city",
            backstory="You are an experienced weather researcher with attention to detail",
            llm=model,
            tools=tools,
            verbose=True,
        )

        my_crew = Crew(
            agents=[agent],
            tasks=[
                Task(
                    description="Find the weather in a specific city",
                    expected_output="Weather in San francisco.",
                    agent=agent
                )
            ],
            verbose=True,
        )

        result = my_crew.kickoff()
        logger.info(result.raw)

if __name__ == "__main__":
    asyncio.run(main())
