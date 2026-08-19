from dataclasses import dataclass, asdict
import json


@dataclass(frozen=True)
class RunEvent:
    """A finished run, shaped for both Postgres and the live stream."""
    agent_id: str
    task_id: str
    score: float
    latency_ms: int
    tool_calls: int
    ts: float

    def to_json(self) -> str:
        return json.dumps(asdict(self))
