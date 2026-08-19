from typing import TypedDict

from langgraph.graph import StateGraph, END
from openai import AsyncOpenAI

from agent.tools import TOOLS, call_tool

client = AsyncOpenAI()


class RunState(TypedDict):
    """The state threaded through the graph as the agent works a task."""
    messages: list[dict]
    tool_calls: int


async def think(state: RunState) -> RunState:
    """One reasoning step: ask the model, which may request a tool."""
    resp = await client.chat.completions.create(
        model="gpt-4o-mini", messages=state["messages"], tools=TOOLS,
    )
    msg = resp.choices[0].message
    state["messages"].append(msg.model_dump())
    if msg.tool_calls:
        for tc in msg.tool_calls:
            result = call_tool(tc.function.name, tc.function.arguments)
            state["messages"].append(
                {"role": "tool", "tool_call_id": tc.id, "content": result}
            )
        state["tool_calls"] += len(msg.tool_calls)
    return state


def should_continue(state: RunState) -> str:
    """Loop back to think while the last message asked for a tool."""
    last = state["messages"][-1]
    return "think" if last.get("role") == "tool" else END


def build_graph():
    g = StateGraph(RunState)
    g.add_node("think", think)
    g.set_entry_point("think")
    g.add_conditional_edges("think", should_continue)
    return g.compile()
