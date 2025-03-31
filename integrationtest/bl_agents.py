import asyncio

from blaxel.agents import bl_agent


async def main():
    agent = bl_agent("vercel-first")
    print(await agent.arun({"inputs": "Hello, world!"}))
    print(agent.run({"inputs": "Hello, world!"}))

if __name__ == "__main__":
    asyncio.run(main())
