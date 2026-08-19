from agent.run_event import RunEvent
from agent.experiments import make_variants, best_variant


def make_event(agent_id: str, task_id: str, score: float) -> RunEvent:
    return RunEvent(agent_id=agent_id, task_id=task_id, score=score,
                    latency_ms=100, tool_calls=1, ts=0.0)


def count_failures(results: list) -> int:
    return sum(1 for r in results if not isinstance(r, RunEvent))


def test_count_failures_splits_events_from_exceptions():
    results = [make_event("a", "t1", 1.0), ValueError("boom"),
               make_event("a", "t2", 0.0)]
    assert count_failures(results) == 1


def test_make_variants_appends_each_instruction():
    variants = make_variants("BASE", {"v1": "be terse", "v2": "show work"})
    assert variants == {"v1": "BASE\n\nbe terse", "v2": "BASE\n\nshow work"}


def test_best_variant_ignores_failures_key():
    wins = {"v1": 2, "v2": 5, "_failures": 9}
    assert best_variant(wins) == "v2"
