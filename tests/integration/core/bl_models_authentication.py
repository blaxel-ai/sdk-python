"""Tests for model authentication with token expiry."""

import asyncio
from typing import Any, Callable, List

import pytest

# Import model functions from different frameworks
try:
    from blaxel.langgraph import bl_model as bl_model_langgraph
except ImportError:
    bl_model_langgraph = None

try:
    from blaxel.llamaindex import bl_model as bl_model_llamaindex
except ImportError:
    bl_model_llamaindex = None

try:
    from blaxel.openai import bl_model as bl_model_openai
except ImportError:
    bl_model_openai = None

try:
    from blaxel.pydantic import bl_model as bl_model_pydantic
except ImportError:
    bl_model_pydantic = None

try:
    from blaxel.crewai import bl_model as bl_model_crewai
except ImportError:
    bl_model_crewai = None

try:
    from blaxel.googleadk import bl_model as bl_model_googleadk
except ImportError:
    bl_model_googleadk = None

try:
    from blaxel.livekit import bl_model as bl_model_livekit
except ImportError:
    bl_model_livekit = None

# Configuration
EXECUTION_MODE = "parallel"  # "parallel" or "sequential"

# Models that support authentication/tokens
MODELS = [
    "gpt-4o-mini",
    "claude-sonnet-4",
    "cerebras-sandbox",
    "cohere-command-r-plus",
    "mistral-large-latest",
    "deepseek-chat",
    "gemini-2-5-pro-preview-06-05",
    "xai-grok-beta",
]

# Frameworks to test - comment out any you don't want to test
FRAMEWORKS = [
    "langgraph",
    "llamaindex",
    "googleadk",
    "openai",
    "crewai",
    "livekit",
    "pydantic",
]


class TestCase:
    """Represents a test case for a specific framework and model."""

    def __init__(
        self,
        framework: str,
        model_name: str,
        model: Any,
        test_func: Callable[[Any, str, int], None],
    ):
        self.framework = framework
        self.model_name = model_name
        self.model = model
        self.test_func = test_func


async def test_langgraph(model: Any, model_name: str, request_num: int) -> None:
    """Test LangGraph framework."""
    try:
        from langchain_core.messages import HumanMessage

        result = await model.ainvoke([HumanMessage(content="Hello, world!")])
        print(f"langgraph, {model_name} (request {request_num}): {result.content}")
    except Exception as e:
        print(f"langgraph, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def test_llamaindex(model: Any, model_name: str, request_num: int) -> None:
    """Test LlamaIndex framework."""
    try:
        # LlamaIndex uses ChatMessage objects, not dicts
        from llama_index.core.llms import ChatMessage, MessageRole

        response = await model.achat(
            messages=[ChatMessage(role=MessageRole.USER, content="Hello, world!")]
        )
        print(f"llamaindex, {model_name} (request {request_num}): {response.message.content}")
    except Exception as e:
        print(f"llamaindex, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def test_pydantic(model: Any, model_name: str, request_num: int) -> None:
    """Test Pydantic AI framework."""
    try:
        from pydantic_ai import Agent

        agent = Agent(model)
        result = await agent.run("Hello, world!")
        print(f"pydantic, {model_name} (request {request_num}): {result.data}")
    except Exception as e:
        print(f"pydantic, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def test_crewai(model: Any, model_name: str, request_num: int) -> None:
    """Test CrewAI framework."""
    try:
        # CrewAI typically works through agents, so we'll create a simple agent
        from crewai import Agent, Crew, Task

        agent = Agent(
            role="Assistant",
            goal="Respond to greetings",
            backstory="You are a helpful assistant",
            llm=model,
        )

        task = Task(
            description="Say hello back",
            expected_output="A greeting response",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task])
        result = await crew.kickoff_async()
        print(f"crewai, {model_name} (request {request_num}): {result}")
    except Exception as e:
        print(f"crewai, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def test_openai(model: Any, model_name: str, request_num: int) -> None:
    """Test OpenAI framework."""
    try:
        from agents import ModelSettings, ModelTracing

        result = await model.get_response(
            None, "Hello, world!", ModelSettings(), [], None, [], ModelTracing(0), None, None
        )
        print(f"openai, {model_name} (request {request_num}): {result.output[0].content[0].text}")
    except Exception as e:
        print(f"openai, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def test_googleadk(model: Any, model_name: str, request_num: int) -> None:
    """Test Google ADK framework."""
    try:
        from google.adk.models.llm_request import LlmRequest

        request = LlmRequest(
            model=model_name,
            contents=[{"role": "user", "parts": [{"text": "Hello, world!"}]}],
            config={},
            tools_dict={},
        )
        async for result in model.generate_content_async(request):
            print(f"googleadk, {model_name} (request {request_num}): {result}")

    except Exception as e:
        print(f"googleadk, {model_name} (request {request_num}): Error - {str(e)}")


async def test_livekit(model: Any, model_name: str, request_num: int) -> None:
    """Test Livekit framework."""
    from livekit.agents.llm.chat_context import ChatContext, ChatMessage
    from livekit.agents.llm.tool_context import function_tool
    from livekit.agents.types import APIConnectOptions

    async def fake_tool():
        return "Hello, world!"

    try:
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
        print(f"livekit, {model_name} (request {request_num}): {content}")
    except Exception as e:
        print(f"livekit, {model_name} (request {request_num}): Error - {str(e)}")
        raise


async def run_parallel(test_cases: List[TestCase]) -> None:
    """Run all test cases in parallel mode."""
    print("\n=== Running first requests in parallel ===")

    # Run all first requests in parallel
    first_requests = []
    for test_case in test_cases:

        async def run_test(tc=test_case):
            try:
                await tc.test_func(tc.model, tc.model_name, 1)
            except Exception as e:
                print(f"Error in first request for {tc.framework}, {tc.model_name}: {e}")

        first_requests.append(run_test())

    await asyncio.gather(*first_requests)

    print("\n=== Waiting 40s for tokens to expire... ===")
    await asyncio.sleep(40)  # wait 40s, token will expire

    print("\n=== Running second requests in parallel (after token expiry) ===")

    # Run all second requests in parallel
    second_requests = []
    for test_case in test_cases:

        async def run_test(tc=test_case):
            try:
                await tc.test_func(tc.model, tc.model_name, 2)
            except Exception as e:
                print(f"Error in second request for {tc.framework}, {tc.model_name}: {e}")

        second_requests.append(run_test())

    await asyncio.gather(*second_requests)


async def run_sequential(test_cases: List[TestCase]) -> None:
    """Run all test cases in sequential mode."""
    print("\n=== Running requests sequentially with 40s between each call ===")

    call_number = 0
    for i, test_case in enumerate(test_cases):
        call_number += 1

        # First request
        print(
            f"\n--- Call {call_number}: {test_case.framework}, {test_case.model_name} (request 1) ---"
        )
        try:
            await test_case.test_func(test_case.model, test_case.model_name, 1)
        except Exception as e:
            print(f"Error in first request for {test_case.framework}, {test_case.model_name}: {e}")

        print("Waiting 40s before next call...")
        await asyncio.sleep(40)

        # Second request
        call_number += 1
        print(
            f"\n--- Call {call_number}: {test_case.framework}, {test_case.model_name} (request 2 after token expiry) ---"
        )
        try:
            await test_case.test_func(test_case.model, test_case.model_name, 2)
        except Exception as e:
            print(f"Error in second request for {test_case.framework}, {test_case.model_name}: {e}")

        # Wait 40s before next model (if not the last one)
        if i < len(test_cases) - 1:
            print("Waiting 40s before next model...")
            await asyncio.sleep(40)


async def prepare_test_cases() -> List[TestCase]:
    """Prepare all test cases based on available frameworks and models."""
    test_cases = []

    for model_name in MODELS:
        try:
            # LangGraph framework
            if "langgraph" in FRAMEWORKS and bl_model_langgraph:
                print(f"Loading langgraph model: {model_name}")
                try:
                    model = await bl_model_langgraph(model_name)
                    test_cases.append(TestCase("langgraph", model_name, model, test_langgraph))
                except Exception as e:
                    print(f"Failed to load langgraph {model_name}: {e}")

            # LlamaIndex framework
            if "llamaindex" in FRAMEWORKS and bl_model_llamaindex:
                print(f"Loading llamaindex model: {model_name}")
                try:
                    model = await bl_model_llamaindex(model_name)
                    test_cases.append(TestCase("llamaindex", model_name, model, test_llamaindex))
                except Exception as e:
                    print(f"Failed to load llamaindex {model_name}: {e}")

            # OpenAI framework
            if "openai" in FRAMEWORKS and bl_model_openai:
                print(f"Loading openai model: {model_name}")
                try:
                    model = await bl_model_openai(model_name)
                    test_cases.append(TestCase("openai", model_name, model, test_openai))
                except Exception as e:
                    print(f"Failed to load openai {model_name}: {e}")

            # Pydantic framework
            if "pydantic" in FRAMEWORKS and bl_model_pydantic:
                print(f"Loading pydantic model: {model_name}")
                try:
                    model = await bl_model_pydantic(model_name)
                    test_cases.append(TestCase("pydantic", model_name, model, test_pydantic))
                except Exception as e:
                    print(f"Failed to load pydantic {model_name}: {e}")

            # CrewAI framework
            if "crewai" in FRAMEWORKS and bl_model_crewai:
                print(f"Loading crewai model: {model_name}")
                try:
                    model = await bl_model_crewai(model_name)
                    test_cases.append(TestCase("crewai", model_name, model, test_crewai))
                except Exception as e:
                    print(f"Failed to load crewai {model_name}: {e}")

            # Google ADK framework
            if "googleadk" in FRAMEWORKS and bl_model_googleadk:
                print(f"Loading googleadk model: {model_name}")
                try:
                    model = await bl_model_googleadk(model_name)
                    test_cases.append(TestCase("googleadk", model_name, model, test_googleadk))
                except Exception as e:
                    print(f"Failed to load googleadk {model_name}: {e}")

            # Livekit framework
            if "livekit" in FRAMEWORKS and bl_model_livekit:
                print(f"Loading livekit model: {model_name}")
                try:
                    model = await bl_model_livekit(model_name)
                    test_cases.append(TestCase("livekit", model_name, model, test_livekit))
                except Exception as e:
                    print(f"Failed to load livekit {model_name}: {e}")

        except Exception as e:
            print(f"Error loading {model_name}: {e}")

    return test_cases


@pytest.mark.asyncio
@pytest.mark.integration
async def test_model_authentication():
    """Main test function for model authentication with token expiry."""
    # Prepare all test cases
    test_cases = await prepare_test_cases()

    if not test_cases:
        pytest.skip("No test cases available to run")

    print(f"\n=== Testing {len(MODELS)} model(s) with {len(FRAMEWORKS)} framework(s) ===")
    print(f"Models: {', '.join(MODELS)}")
    print(f"Frameworks: {', '.join(FRAMEWORKS)}")
    print(f"Execution mode: {EXECUTION_MODE}")

    # Run tests based on execution mode
    if EXECUTION_MODE == "parallel":
        await run_parallel(test_cases)
    else:
        await run_sequential(test_cases)

    print("\n=== All tests completed ===")


if __name__ == "__main__":
    """Allow running the test directly as a script."""

    async def main():
        try:
            await test_model_authentication()
        except Exception as e:
            print(f"Error: {e}")
            raise

    asyncio.run(main())
