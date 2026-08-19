-- One row per (agent, task) evaluation — the atomic record we aggregate.
CREATE TABLE IF NOT EXISTS runs (
    id          BIGSERIAL PRIMARY KEY,
    agent_id    TEXT        NOT NULL,
    task_id     TEXT        NOT NULL,
    score       REAL        NOT NULL,
    latency_ms  INTEGER     NOT NULL,
    tool_calls  INTEGER     NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Leaderboards aggregate by agent, so index that column.
CREATE INDEX IF NOT EXISTS idx_runs_agent ON runs (agent_id);
