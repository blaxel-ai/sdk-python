import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.core.jobs import bl_job

logger = getLogger(__name__)


async def main():
    """Main function for standalone execution."""
    job = bl_job("myjob")

    # Test async functionality
    print("Testing async bl_job...")
    result = await job.arun([{"name": "charlou", "age": 25}])
    logger.info(f"Async result: {result}")
    print(f"Async result: {result}")

    # Test sync functionality
    print("\nTesting sync bl_job...")
    result = job.run([{"name": "charlou", "age": 25}])
    logger.info(f"Sync result: {result}")
    print(f"Sync result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
