import time

from agent.graph import build_graph
from agent.tasks import Task
from agent.run_event import RunEvent

_graph = build_graph()


def _final_answer(messages: list[dict]) -> str:
    """The last assistant message with text content is the agent's answer."""
    for msg in reversed(messages):
        if msg.get("role") == "assistant" and msg.get("content"):
            return msg["content"]
    return ""


async def run_once(agent_id: str, system_prompt: str, task: Task) -> RunEvent:
    """Run ONE agent on ONE task: execute, grade, and time it."""
    state = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task.prompt},
        ],
        "tool_calls": 0,
    }
    started = time.perf_counter()
    result = await _graph.ainvoke(state)
    latency_ms = int((time.perf_counter() - started) * 1000)

    answer = _final_answer(result["messages"])
    return RunEvent(
        agent_id=agent_id,
        task_id=task.id,
        score=task.grade(answer),
        latency_ms=latency_ms,
        tool_calls=result["tool_calls"],
        ts=time.time(),
    )
