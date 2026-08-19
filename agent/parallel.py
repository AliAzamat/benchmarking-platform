import asyncio

from agent.tasks import Task
from agent.runner import run_once
from agent.run_event import RunEvent
from gateway.bus import publish_run


async def _bounded_run(
    sem: asyncio.Semaphore, agent_id: str, prompt: str, task: Task
) -> RunEvent:
    """Run one (agent, task) pair, then publish it live before returning."""
    async with sem:
        event = await run_once(agent_id, prompt, task)
    await publish_run(event)  # announce it the instant it finishes
    return event


async def run_matrix(
    agents: dict[str, str],          # agent_id -> system_prompt
    tasks: list[Task],
    max_concurrency: int = 50,
) -> tuple[list[RunEvent], int]:
    """Run EVERY agent over EVERY task in parallel, surviving failures.

    Returns (successful events, number of failures).
    """
    sem = asyncio.Semaphore(max_concurrency)
    coros = [
        _bounded_run(sem, agent_id, prompt, task)
        for agent_id, prompt in agents.items()
        for task in tasks
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    events = [r for r in results if isinstance(r, RunEvent)]
    failures = len(results) - len(events)
    return events, failures
