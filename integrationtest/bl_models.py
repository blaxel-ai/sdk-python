import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from pydantic_ai.messages import ModelRequest, UserPromptPart
from pydantic_ai.models import ModelRequestParameters, ModelSettings

from blaxel.models import bl_model

logger = getLogger(__name__)


MODEL = "gpt-4o-mini"
# MODEL = "claude-3-5-sonnet"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus"
# MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"
# MODEL = "cerebras-llama-4-scout-17b"

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

async def test_model_pydantic():
    model = await bl_model(MODEL).to_pydantic()
    result = await model.request(
        [ModelRequest(parts=[UserPromptPart(content="Hello, world!")])],
        model_settings=ModelSettings(max_tokens=100),
        model_request_parameters=ModelRequestParameters(function_tools=[], allow_text_result=True, result_tools=[])
    )
    logger.info(result)

async def test_model_google_adk():
    from google.adk.models.llm_request import LlmRequest

    model = await bl_model(MODEL).to_google_adk()
    request = LlmRequest(
        model=MODEL,
        contents=[{"role": "user", "parts": [{"text": "Hello, world!"}]}],
        config={},
        tools_dict={},
    )
    async for result in model.generate_content_async(request):
        logger.info(result)

async def main():
    # await test_model_langchain()
    # await test_model_llamaindex()
    # await test_model_crewai()
    # await test_model_pydantic()
    await test_model_google_adk()

if __name__ == "__main__":
    asyncio.run(main())