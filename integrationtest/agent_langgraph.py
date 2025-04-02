import asyncio

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt
from typing_extensions import Literal

from blaxel.models import bl_model
from blaxel.tools import bl_tools


class State(MessagesState):
    """Simple state."""

async def create_agent_graph(tools):
    builder = StateGraph(State)

    def human_review_node(state) -> Command[Literal["call_llm", "run_tool"]]:
        last_message = state["messages"][-1]
        tool_call = last_message.tool_calls[-1]

        # this is the value we'll be providing via Command(resume=<human_review>)
        human_review = interrupt(
            {
                "question": "Is this correct?",
                # Surface tool calls for review
                "tool_call": tool_call,
            }
        )

        review_action = human_review["action"]
        review_data = human_review.get("data")

        # if approved, call the tool
        if review_action == "continue":
            return Command(goto="run_tool")

        # update the AI message AND call tools
        elif review_action == "update":
            updated_message = {
                "role": "ai",
                "content": last_message.content,
                "tool_calls": [
                    {
                        "id": tool_call["id"],
                        "name": tool_call["name"],
                        # This the update provided by the human
                        "args": review_data,
                    }
                ],
                # This is important - this needs to be the same as the message you replacing!
                # Otherwise, it will show up as a separate message
                "id": last_message.id,
            }
            return Command(goto="run_tool", update={"messages": [updated_message]})

        # provide feedback to LLM
        elif review_action == "feedback":
            # NOTE: we're adding feedback message as a ToolMessage
            # to preserve the correct order in the message history
            # (AI messages with tool calls need to be followed by tool call messages)
            tool_message = {
                "role": "tool",
                # This is our natural language feedback
                "content": review_data,
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
            return Command(goto="call_llm", update={"messages": [tool_message]})

    def route_after_llm(state) -> Literal["__end__", "human_review_node"]:
        if len(state["messages"][-1].tool_calls) == 0:
            return END
        else:
            return "human_review_node"


    async def call_llm(state):
        model = await bl_model("gpt-4o-mini", temperature=0).to_langchain()
        model = model.bind_tools(tools)
        return {"messages": [model.invoke(state["messages"])]}


    builder.add_node("call_llm", call_llm)
    builder.add_node("run_tool", ToolNode(tools))
    builder.add_node("human_review_node", human_review_node)

    builder.set_entry_point("call_llm")
    builder.add_conditional_edges("call_llm", route_after_llm)
    builder.add_edge("run_tool", "call_llm")

    # Set up memory
    memory = MemorySaver()

    # Add
    graph = builder.compile(checkpointer=memory)

    # View
    print(graph.get_graph().draw_ascii())
    return graph



async def run_graphs():
    tools = await bl_tools(["blaxel-search"]).to_langchain()
    graph = await create_agent_graph(tools)

    # With no tool call
    initial_input = {"messages": [{"role": "user", "content": "hi!"}]}
    thread = {"configurable": {"thread_id": "1"}}
    async for event in graph.astream(initial_input, thread, stream_mode="updates"):
        print(event)
        print("\n")


    # With a tool call, should make interupt

    # Run the graph until the first interruption
    initial_input = {"messages": [{"role": "user", "content": "what's the weather in sf?"}]}
    thread = {"configurable": {"thread_id": "2"}}
    async for event in graph.astream(initial_input, thread, stream_mode="updates"):
        print(event)
        print("\n")


    # Pending Executions!
    print("Pending Executions!")
    print(graph.get_state(thread).next)

    # Resume the pending interupt
    async for event in graph.astream(
        # provide value
        Command(resume={"action": "continue"}),
        thread,
        stream_mode="updates",
    ):
        print(event)
        print("\n")

asyncio.run(run_graphs())