import asyncio

from blaxel.jobs import bl_job


async def main():
    job = bl_job("myjob")
    print(await job.arun([{"name": "charlou", "age": 25}]))
    print(job.run([{"name": "charlou", "age": 25}]))

if __name__ == "__main__":
    asyncio.run(main())
