import asyncio
import os

from dotenv import load_dotenv

load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"

from logging import getLogger

from blaxel.models import bl_model

logger = getLogger(__name__)


async def test_openai():
    model = await bl_model("gpt-4o-mini").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_anthropic():
    model = await bl_model("claude-3-5-sonnet").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_xai():
    model = await bl_model("xai-grok-beta").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_cohere():
    model = await bl_model("cohere-command-r-plus").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_deepseek():
    model = await bl_model("deepseek-chat").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_gemini():
    model = await bl_model("gemini-2-0-flash").to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def main():
    # await test_openai()
    # await test_anthropic()
    # await test_xai()
    # await test_cohere()
    # await test_deepseek()
    await test_gemini()

if __name__ == "__main__":
    asyncio.run(main())