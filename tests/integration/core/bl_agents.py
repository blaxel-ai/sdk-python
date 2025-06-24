import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.core.agents import bl_agent

logger = getLogger(__name__)


async def main():
    """Main function for standalone execution."""
    agent = bl_agent("template-google-adk-py")

    # Test async functionality
    print("Testing async bl_agent...")
    result = await agent.arun({"inputs": "Hello, world!"})
    logger.info(f"Async result: {result}")
    print(f"Async result: {result}")

    # Test sync functionality
    print("\nTesting sync bl_agent...")
    result = agent.run({"inputs": "Hello, world!"})
    logger.info(f"Sync result: {result}")
    print(f"Sync result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
