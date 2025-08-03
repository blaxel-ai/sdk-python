import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from agents import ModelSettings, ModelTracing
from pydantic_ai.messages import ModelRequest, UserPromptPart
from pydantic_ai.models import ModelRequestParameters

logger = getLogger(__name__)

# MODEL = "gpt-4o-mini"
# MODEL = "claude-3-5-sonnet"
MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus"
# MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"
# MODEL = "cerebras-llama-4-scout-17b"


async def test_model_langchain():
    """Test bl_model to_langchain conversion."""
    from blaxel.langgraph import bl_model as bl_model_langgraph

    print("Testing LangChain model conversion...")
    model = await bl_model_langgraph(MODEL)
    result = await model.ainvoke("Hello, world!")
    logger.info(f"LangChain result: {result}")
    print(f"LangChain result: {result}")


async def test_model_llamaindex():
    """Test bl_model to_llamaindex conversion."""
    from blaxel.llamaindex import bl_model as bl_model_llamaindex

    print("Testing LlamaIndex model conversion...")
    model = await bl_model_llamaindex(MODEL)
    result = await model.acomplete("Hello, world!")
    logger.info(f"LlamaIndex result: {result}")
    print(f"LlamaIndex result: {result}")


async def test_model_crewai():
    """Test bl_model to_crewai conversion."""
    from blaxel.crewai import bl_model as bl_model_crewai

    print("Testing CrewAI model conversion...")
    # Note: not working with cohere
    model = await bl_model_crewai(MODEL)
    result = model.call([{"role": "user", "content": "Hello, world!"}])
    logger.info(f"CrewAI result: {result}")
    print(f"CrewAI result: {result}")


async def test_model_pydantic():
    """Test bl_model to_pydantic conversion."""
    from blaxel.pydantic import bl_model as bl_model_pydantic

    print("Testing Pydantic model conversion...")
    model = await bl_model_pydantic(MODEL)
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
    from blaxel.googleadk import bl_model as bl_model_googleadk

    print("Testing Google ADK model conversion...")
    from google.adk.models.llm_request import LlmRequest

    model = await bl_model_googleadk(MODEL)
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


async def test_openai() -> None:
    """Test OpenAI framework."""
    try:
        from blaxel.openai import bl_model as bl_model_openai

        model = await bl_model_openai(MODEL)
        result = await model.get_response(
            None, "Hello, world!", ModelSettings(), [], None, [], ModelTracing(0), None, None
        )
        print(f"openai: {result.output[0].content[0].text}")
    except Exception as e:
        print(f"openai: Error - {str(e)}")
        raise


async def test_livekit():
    """Test Livekit framework."""
    from livekit.agents.llm.chat_context import ChatContext, ChatMessage
    from livekit.agents.llm.tool_context import function_tool
    from livekit.agents.types import APIConnectOptions

    from blaxel.livekit import bl_model as bl_model_livekit

    async def fake_tool():
        return "Hello, world!"

    model = await bl_model_livekit(MODEL)
    result = model.chat(
        chat_ctx=ChatContext([ChatMessage(role="user", content=["Hello, world!"])]),
        tools=[function_tool(fake_tool)],
        conn_options=APIConnectOptions(),
        parallel_tool_calls=False,
        tool_choice="auto",
    )
    content = ""
    async for chunk in result:
        if chunk.delta and chunk.delta.content:
            content += chunk.delta.content
    print(f"livekit: {content}")


async def main():
    """Main function for standalone execution."""
    # await test_model_langchain()
    # await test_model_llamaindex()
    # await test_model_crewai()
    # await test_model_pydantic()
    # await test_model_google_adk()
    # await test_openai()
    await test_livekit()


if __name__ == "__main__":
    asyncio.run(main())
