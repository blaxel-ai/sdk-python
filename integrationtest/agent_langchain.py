import asyncio

from dotenv import load_dotenv

load_dotenv()

from logging import getLogger

from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent

from blaxel.models import bl_model
from blaxel.tools import bl_tools

logger = getLogger(__name__)

MODEL = "gpt-4o-mini"
# MODEL = "claude-3-5-sonnet"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus" # x -> tool call not supported
# MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"

async def main():
    tools = await bl_tools(["blaxel-search"]).to_langchain()

    model = await bl_model(MODEL, temperature=0).to_langchain()

    agent = create_react_agent(model=model, tools=tools, prompt="You are a helpful assistant. Maximum number of tool call is 1")
    input = "Search online for the current weather in San Francisco ?"
    # input = "What are the tools in your arsenal ?"
    # input = "Hello world"
    messages = {"messages": [("user", input)]}
    responses = []
    async for message in agent.astream(messages):
        if "agent" in message and len(message["agent"].get("messages", [])) > 0:
            msg = message["agent"].get("messages", [])[0]
            if isinstance(msg, AIMessage):
                if msg.additional_kwargs:
                    if msg.additional_kwargs.get("tool_calls"):
                        for tool_call in msg.additional_kwargs.get("tool_calls"):
                            fn = tool_call.get("function", {})
                            if fn:
                                logger.info(f"Tool request: {fn['name']} with arguments {fn['arguments']}")
        responses.append(message)

    logger.info(responses[-1]["agent"]["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())