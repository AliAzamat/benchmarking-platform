from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Task:
    """One unit of work an agent is evaluated on, plus how to grade an answer."""
    id: str
    prompt: str
    grade: Callable[[str], float]  # answer -> score in [0, 1]


def _contains(expected: str) -> Callable[[str], float]:
    """Grader factory: 1.0 if the expected substring appears, else 0.0."""
    def grader(answer: str) -> float:
        return 1.0 if expected.lower() in answer.lower() else 0.0
    return grader


# A deliberately HETEROGENEOUS suite: arithmetic, retrieval, and reasoning.
TASK_SUITE: list[Task] = [
    Task("math-1", "What is 17 * 23?", _contains("391")),
    Task("kb-1", "What is the capital of France?", _contains("Paris")),
    Task("reason-1", "If all blorps are greeps and Bob is a blorp, is Bob a greep?",
         _contains("yes")),
]
