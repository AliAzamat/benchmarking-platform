import asyncpg

from agent.run_event import RunEvent

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn="postgresql://localhost/eval")
    return _pool


async def save_events(events: list[RunEvent]) -> int:
    """Insert MANY runs in one round trip and one transaction."""
    if not events:
        return 0
    pool = await get_pool()
    rows = [
        (e.agent_id, e.task_id, e.score, e.latency_ms, e.tool_calls)
        for e in events
    ]
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(
                "INSERT INTO runs "
                "(agent_id, task_id, score, latency_ms, tool_calls) "
                "VALUES ($1, $2, $3, $4, $5)",
                rows,
            )
    return len(rows)
