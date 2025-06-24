import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from pydantic_ai.messages import ModelRequest, UserPromptPart
from pydantic_ai.models import ModelRequestParameters, ModelSettings

from blaxel.core.models import bl_model

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
    """Test bl_model to_langchain conversion."""
    print("Testing LangChain model conversion...")
    model = await bl_model(MODEL).to_langchain()
    result = await model.ainvoke("Hello, world!")
    logger.info(f"LangChain result: {result}")
    print(f"LangChain result: {result}")


async def test_model_llamaindex():
    """Test bl_model to_llamaindex conversion."""
    print("Testing LlamaIndex model conversion...")
    model = await bl_model(MODEL).to_llamaindex()
    result = await model.acomplete("Hello, world!")
    logger.info(f"LlamaIndex result: {result}")
    print(f"LlamaIndex result: {result}")


async def test_model_crewai():
    """Test bl_model to_crewai conversion."""
    print("Testing CrewAI model conversion...")
    # Note: not working with cohere
    model = await bl_model(MODEL).to_crewai()
    result = model.call([{"role": "user", "content": "Hello, world!"}])
    logger.info(f"CrewAI result: {result}")
    print(f"CrewAI result: {result}")


async def test_model_pydantic():
    """Test bl_model to_pydantic conversion."""
    print("Testing Pydantic model conversion...")
    model = await bl_model(MODEL).to_pydantic()
    result = await model.request(
        [ModelRequest(parts=[UserPromptPart(content="Hello, world!")])],
        model_settings=ModelSettings(max_tokens=100),
        model_request_parameters=ModelRequestParameters(
            function_tools=[], allow_text_result=True, result_tools=[]
        ),
    )
    logger.info(f"Pydantic result: {result}")
    print(f"Pydantic result: {result}")


async def test_model_google_adk():
    """Test bl_model to_google_adk conversion."""
    print("Testing Google ADK model conversion...")
    from google.adk.models.llm_request import LlmRequest

    model = await bl_model(MODEL).to_google_adk()
    request = LlmRequest(
        model=MODEL,
        contents=[{"role": "user", "parts": [{"text": "Hello, world!"}]}],
        config={},
        tools_dict={},
    )
    results = []
    async for result in model.generate_content_async(request):
        results.append(result)
        logger.info(f"Google ADK result: {result}")
        print(f"Google ADK result: {result}")


async def main():
    """Main function for standalone execution."""
    await test_model_langchain()
    await test_model_llamaindex()
    await test_model_crewai()
    await test_model_pydantic()
    await test_model_google_adk()


if __name__ == "__main__":
    asyncio.run(main())
