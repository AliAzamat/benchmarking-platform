-- Rank agents: highest mean score first, ties broken by lowest latency.
SELECT
    agent_id,
    COUNT(*)              AS n_runs,
    AVG(score)            AS mean_score,
    AVG(latency_ms)       AS mean_latency_ms,
    AVG(tool_calls)       AS mean_tool_calls,
    RANK() OVER (
        ORDER BY AVG(score) DESC, AVG(latency_ms) ASC
    )                     AS rank
FROM runs
GROUP BY agent_id
ORDER BY rank;
