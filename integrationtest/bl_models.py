import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from blaxel.models import bl_model

logger = getLogger(__name__)


MODEL = "gpt-4o-mini"
# MODEL = "claude-3-5-sonnet"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus"
# MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"

async def test_model_langchain():
    model = await bl_model(MODEL).to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(result)

async def test_model_llamaindex():
    model = await bl_model(MODEL).to_llamaindex()
    result = await model.acomplete("Hello, world!")
    logger.info(result)

async def test_model_crewai():
    # not working: cohere
    model = await bl_model(MODEL).to_crewai()
    result = model.call([{"role": "user", "content": "Hello, world!"}])
    logger.info(result)

async def main():
    await test_model_langchain()
    await test_model_llamaindex()
    await test_model_crewai()

if __name__ == "__main__":
    asyncio.run(main())