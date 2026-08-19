from agent.tasks import TASK_SUITE
from agent.parallel import run_matrix
from agent.store import save_events


def make_variants(base: str, instructions: dict[str, str]) -> dict[str, str]:
    """Build prompt variants: each is the base prompt plus one tweak.

    Returns {variant_id: system_prompt}.
    """
    return {vid: f"{base}\n\n{extra}" for vid, extra in instructions.items()}


async def run_experiment(base: str, instructions: dict[str, str]) -> dict[str, int]:
    """Evaluate every prompt variant over the whole suite, persist, and report wins."""
    agents = make_variants(base, instructions)
    events, failures = await run_matrix(agents, TASK_SUITE)
    await save_events(events)

    wins: dict[str, int] = {vid: 0 for vid in agents}
    for task in TASK_SUITE:
        best, top = None, -1.0
        for vid in agents:
            score = next(
                (e.score for e in events
                 if e.agent_id == vid and e.task_id == task.id), -1.0
            )
            if score > top:
                best, top = vid, score
        if best is not None:
            wins[best] += 1
    wins["_failures"] = failures
    return wins
